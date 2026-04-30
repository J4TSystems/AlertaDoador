import json
import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from dtos.stock_dto import BloodStockDTO
from models.blood_stock_model import BloodStock, BloodType, StockStatus
from repositories.stock_repository import StockRepository


class StockService:
    def __init__(self, repository: StockRepository):
        self.repository = repository

    def get_all_stock_levels(self) -> List[BloodStockDTO]:
        """
        Return a hardcoded list of 1 or 2 BloodStockDTO objects.
        """
        return [
            BloodStockDTO(
                blood_type=BloodType.A_POS,
                status=StockStatus.STABLE,
                last_updated=datetime.now(),
            ),
            BloodStockDTO(
                blood_type=BloodType.O_NEG,
                status=StockStatus.CRITICAL,
                last_updated=datetime.now(),
            ),
        ]

    def sync_with_external_source(self) -> List[BloodStockDTO]:
        """
        Sync blood stock data from an external source.
        """
        referencia, estoque_padrao = self._prosangue_scrape()
        if not referencia or not estoque_padrao:
            return []

        mapping = {
            "A-": {"ref": "A_negativo", "enum": BloodType.A_NEG},
            "A+": {"ref": "A_positivo", "enum": BloodType.A_POS},
            "B-": {"ref": "B_negativo", "enum": BloodType.B_NEG},
            "B+": {"ref": "B_positivo", "enum": BloodType.B_POS},
            "AB-": {"ref": "AB_negativo", "enum": BloodType.AB_NEG},
            "AB+": {"ref": "AB_positivo", "enum": BloodType.AB_POS},
            "O-": {"ref": "O_negativo", "enum": BloodType.O_NEG},
            "O+": {"ref": "O_positivo", "enum": BloodType.O_POS},
        }

        dtos = []
        tipos_sanguineos = estoque_padrao.get("tipos_sanguineos", {})
        now = datetime.now()

        for blood_str, map_info in mapping.items():
            qty = tipos_sanguineos.get(blood_str, {}).get("quantidade", 0)
            ref = referencia.get(map_info["ref"], {})

            status = self._results_classify(qty, ref)

            dto = BloodStockDTO(
                blood_type=map_info["enum"], status=status, last_updated=now
            )
            dtos.append(dto)

            # Upsert no repositório
            model = BloodStock(
                blood_type=dto.blood_type,
                status=dto.status,
                last_updated=dto.last_updated,
            )
            self.repository.upsert(model)

        return dtos

    def _prosangue_scrape(self) -> tuple[dict, dict]:
        """
        Scrape data from Pró-Sangue website.
        """
        url = "https://prosangue.sp.gov.br/reqestoque/posicao_estoque.php"
        try:
            # Aumentando o timeout para evitar problemas em ambientes lentos
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return {}, {}

        soup = BeautifulSoup(response.text, "html.parser")

        script_tag = soup.find("script", string=re.compile("referenciaEstoque"))
        if not script_tag:
            return {}, {}

        script_content = script_tag.string

        ref_match = re.search(
            r"const referenciaEstoque = (\{.*?\});", script_content, re.DOTALL
        )
        stock_match = re.search(
            r"const dadosEstoquePadrao = (\{.*?\});", script_content, re.DOTALL
        )

        if not ref_match or not stock_match:
            return {}, {}

        referencia = self._clean_js_to_dict(ref_match.group(1))
        estoque_padrao = self._clean_js_to_dict(stock_match.group(1))

        return referencia, estoque_padrao

    def _results_classify(self, qty: int, ref: dict) -> StockStatus:
        """
        Classify stock level based on quantity and reference values.
        """
        if qty <= ref.get("critico", 0):
            return StockStatus.CRITICAL
        elif qty <= ref.get("alerta", 0):
            return StockStatus.ALERT
        else:
            return StockStatus.STABLE

    def _clean_js_to_dict(self, js_str: str) -> dict:
        js_str = re.sub(r"new Date\(\).*?,", '"fixed_date",', js_str)
        js_str = re.sub(r"(\w+):", r'"\1":', js_str)
        js_str = re.sub(r":\s*0(\d+)", r": \1", js_str)
        js_str = re.sub(r",\s*}", "}", js_str)
        return json.loads(js_str)
