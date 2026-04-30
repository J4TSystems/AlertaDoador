import unittest
from unittest.mock import MagicMock, patch

from models.blood_stock_model import BloodType, StockStatus
from services.stock_service import StockService


class TestStockService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = StockService(self.mock_repo)

    @patch("requests.get")
    def test_sync_with_external_source_success(self, mock_get):
        # Mock HTML content
        html_content = """
        <html>
            <script>
                const referenciaEstoque = {
                    A_positivo: { critico: 10, alerta: 20 },
                    A_negativo: { critico: 5, alerta: 10 },
                    B_positivo: { critico: 10, alerta: 20 },
                    B_negativo: { critico: 5, alerta: 10 },
                    AB_positivo: { critico: 10, alerta: 20 },
                    AB_negativo: { critico: 5, alerta: 10 },
                    O_positivo: { critico: 10, alerta: 20 },
                    O_negativo: { critico: 5, alerta: 10 }
                };
                const dadosEstoquePadrao = {
                    tipos_sanguineos: {
                        "A+": { quantidade: 15 },
                        "A-": { quantidade: 3 },
                        "B+": { quantidade: 25 },
                        "B-": { quantidade: 7 },
                        "AB+": { quantidade: 5 },
                        "AB-": { quantidade: 5 },
                        "O+": { quantidade: 30 },
                        "O-": { quantidade: 2 }
                    }
                };
            </script>
        </html>
        """
        mock_response = MagicMock()
        mock_response.text = html_content
        mock_get.return_value = mock_response

        # Execute sync
        result = self.service.sync_with_external_source()

        # Assertions
        self.assertEqual(len(result), 8)

        # Check A+ (15 is between 10 and 20, so ALERT)
        a_pos = next(item for item in result if item.blood_type == BloodType.A_POS)
        self.assertEqual(a_pos.status, StockStatus.ALERT)

        # Check A- (3 is below 5, so CRITICAL)
        a_neg = next(item for item in result if item.blood_type == BloodType.A_NEG)
        self.assertEqual(a_neg.status, StockStatus.CRITICAL)

        # Check B+ (25 is above 20, so STABLE)
        b_pos = next(item for item in result if item.blood_type == BloodType.B_POS)
        self.assertEqual(b_pos.status, StockStatus.STABLE)

        # Check upsert was called for each
        self.assertEqual(self.mock_repo.upsert.call_count, 8)

    @patch("requests.get")
    def test_sync_with_external_source_no_script(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        result = self.service.sync_with_external_source()
        self.assertEqual(len(result), 0)
        self.mock_repo.upsert.assert_not_called()

    def test_get_all_stock_levels(self):
        from datetime import datetime

        from models.blood_stock_model import BloodStock

        # Mock repository return
        mock_stock = BloodStock(
            blood_type=BloodType.A_POS,
            status=StockStatus.STABLE,
            last_updated=datetime.now(),
        )
        self.mock_repo.get_all.return_value = [mock_stock]

        # Execute
        result = self.service.get_all_stock_levels()

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].blood_type, BloodType.A_POS)
        self.assertEqual(result[0].status, StockStatus.STABLE)
        self.mock_repo.get_all.assert_called_once()


if __name__ == "__main__":
    unittest.main()
