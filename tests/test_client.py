import unittest
from unittest.mock import patch, Mock
from finbro import FinbroClient, FinancialMetric


class TestFinbroClient(unittest.TestCase):
    def setUp(self):
        self.client = FinbroClient()

    @patch('requests.get')
    def test_get_financial_metrics_success(self, mock_get):
        # Mock response data
        mock_data = [
            {
                "ticker": "AAPL",
                "year": 2020,
                "revenue": 274515000000,
                "gross_profit": 104956000000,
                "operating_income": 66288000000,
                "net_income": 57411000000,
                "cash_from_operations": 80674000000,
                "cash_from_financing": -89789000000,
                "cash_from_investing": 3566000000,
                "capital_expenditure": -7309000000,
                "share_based_comp": 6829000000,
                "total_assets": 323888000000,
                "total_liabilities": 258549000000,
                "stockholders_equity": 65339000000,
                "long_term_debt": 92585000000,
                "shares_outstanding": 16976000000,
                "last_updated": "2023-01-01"
            },
            {
                "ticker": "AAPL",
                "year": 2021,
                "revenue": 365817000000,
                "gross_profit": 152836000000,
                "operating_income": 108949000000,
                "net_income": 94680000000,
                "cash_from_operations": 104038000000,
                "cash_from_financing": -93353000000,
                "cash_from_investing": 14545000000,
                "capital_expenditure": -11085000000,
                "share_based_comp": 7906000000,
                "total_assets": 351002000000,
                "total_liabilities": 287912000000,
                "stockholders_equity": 63090000000,
                "long_term_debt": 109106000000,
                "shares_outstanding": 16406000000,
                "last_updated": "2023-01-01"
            }
        ]
        
        # Configure the mock
        mock_response = Mock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_financial_metrics("AAPL")
        
        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], FinancialMetric)
        self.assertEqual(result[0].ticker, "AAPL")
        self.assertEqual(result[0].year, 2020)
        self.assertEqual(result[1].year, 2021)
        
        # Verify the API was called correctly
        mock_get.assert_called_once_with("https://clickhouse.finbro.ai/financial-metrics/AAPL")

    @patch('requests.get')
    def test_get_financial_metrics_validation_error(self, mock_get):
        # Mock response data with invalid field
        mock_data = [
            {
                "ticker": "AAPL",
                "year": "invalid_year",  # Should be int
                "revenue": 274515000000,
                "gross_profit": 104956000000,
                "operating_income": 66288000000,
                "net_income": 57411000000,
                "cash_from_operations": 80674000000,
                "cash_from_financing": -89789000000,
                "cash_from_investing": 3566000000,
                "capital_expenditure": -7309000000,
                "share_based_comp": 6829000000,
                "total_assets": 323888000000,
                "total_liabilities": 258549000000,
                "stockholders_equity": 65339000000,
                "long_term_debt": 92585000000,
                "shares_outstanding": 16976000000,
                "last_updated": "2023-01-01"
            }
        ]
        
        # Configure the mock
        mock_response = Mock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_financial_metrics("AAPL")
        
        # Verify the result (should be empty list as the data is invalid)
        self.assertEqual(len(result), 0)

    @patch('requests.get')
    def test_get_financial_metrics_error(self, mock_get):
        # Configure the mock to raise an exception
        mock_get.side_effect = Exception("API error")
        
        # Call the method
        result = self.client.get_financial_metrics("AAPL")
        
        # Verify the result is None on error
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main() 