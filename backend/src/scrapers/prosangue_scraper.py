import json
import re
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
from models.blood_stock_model import BloodType, StockStatus


class ProSangueScraper:
    _REF_MAPPING = {
        BloodType.A_NEG: "A_negativo",
        BloodType.A_POS: "A_positivo",
        BloodType.B_NEG: "B_negativo",
        BloodType.B_POS: "B_positivo",
        BloodType.AB_NEG: "AB_negativo",
        BloodType.AB_POS: "AB_positivo",
        BloodType.O_NEG: "O_negativo",
        BloodType.O_POS: "O_positivo",
    }

    @staticmethod
    def scrape() -> Tuple[Dict, Dict]:
        """
        Scrape data from Pró-Sangue website.
        """
        url = "https://prosangue.sp.gov.br/reqestoque/posicao_estoque.php"
        try:
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

        referencia = ProSangueScraper._clean_js_to_dict(ref_match.group(1))
        estoque_padrao = ProSangueScraper._clean_js_to_dict(stock_match.group(1))

        return referencia, estoque_padrao

    @staticmethod
    def scrape_mapped_data() -> List[Dict]:
        """
        Scrape data and map it to domain models (BloodType).
        """
        referencia, estoque_padrao = ProSangueScraper.scrape()
        if not referencia or not estoque_padrao:
            return []

        tipos_sanguineos = estoque_padrao.get("tipos_sanguineos", {})
        result = []

        for blood_type, ref_key in ProSangueScraper._REF_MAPPING.items():
            # blood_type.value corresponde a "A-", "A+", etc.
            qty = tipos_sanguineos.get(blood_type.value, {}).get("quantidade", 0)
            ref = referencia.get(ref_key, {})
            result.append({"blood_type": blood_type, "quantity": qty, "reference": ref})

        return result

    @staticmethod
    def _clean_js_to_dict(js_str: str) -> dict:
        js_str = re.sub(r"new Date\(\).*?,", '"fixed_date",', js_str)
        js_str = re.sub(r"(\w+):", r'"\1":', js_str)
        js_str = re.sub(r":\s*0(\d+)", r": \1", js_str)
        js_str = re.sub(r",\s*}", "}", js_str)
        return json.loads(js_str)


class StockClassifier:
    @staticmethod
    def classify(qty: int, ref: dict) -> StockStatus:
        """
        Classify stock level based on quantity and reference values.
        """
        if qty <= ref.get("critico", 0):
            return StockStatus.CRITICAL
        elif qty <= ref.get("alerta", 0):
            return StockStatus.ALERT
        else:
            return StockStatus.STABLE
