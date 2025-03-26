import requests
from typing import List, Optional
from datetime import datetime
from satya import Model, Field

# Enable pretty printing for models
Model.PRETTY_REPR = True

class FinancialMetric(Model):
    """Class representing financial metrics for a company."""
    ticker: str = Field(description="Stock ticker symbol")
    year: int = Field(description="Financial year")
    revenue: float = Field(description="Annual revenue")
    gross_profit: float = Field(description="Gross profit")
    operating_income: float = Field(description="Operating income")
    net_income: float = Field(description="Net income")
    cash_from_operations: float = Field(description="Cash from operations")
    cash_from_financing: float = Field(description="Cash from financing activities")
    cash_from_investing: float = Field(description="Cash from investing activities")
    capital_expenditure: float = Field(description="Capital expenditure")
    share_based_comp: float = Field(description="Share-based compensation")
    total_assets: float = Field(description="Total assets")
    total_liabilities: float = Field(description="Total liabilities")
    stockholders_equity: float = Field(description="Stockholders' equity")
    long_term_debt: float = Field(description="Long-term debt")
    shares_outstanding: float = Field(description="Shares outstanding")
    last_updated: str = Field(description="Last update timestamp")


class FinbroClient:
    """Client for accessing financial metrics from the Finbro API."""
    
    def __init__(self, base_url: str = "https://clickhouse.finbro.ai"):
        """Initialize the Finbro client.
        
        Args:
            base_url: The base URL for the Finbro API.
        """
        self.base_url = base_url
        self.validator = FinancialMetric.validator()
        
    def get_financial_metrics(self, ticker: str) -> Optional[List[FinancialMetric]]:
        """Fetch financial metrics for a given ticker.
        
        Args:
            ticker: The stock ticker symbol.
            
        Returns:
            A list of financial metrics sorted by year (ascending), 
            containing the last 10 years of data. Returns None if the request fails.
        """
        try:
            response = requests.get(f"{self.base_url}/financial-metrics/{ticker}")
            response.raise_for_status()
            data = response.json()
            
            # Validate and convert to FinancialMetric objects
            metrics = []
            for item in data:
                result = self.validator.validate(item)
                if result.is_valid:
                    metrics.append(FinancialMetric(**result.value))
                else:
                    print(f"Validation error for {ticker} data: {result.errors}")
            
            # Sort by year in ascending order and take the last 10 years
            sorted_metrics = sorted(metrics, key=lambda x: x.year)[-10:]
            
            return sorted_metrics
        except Exception as e:
            print(f"Error fetching financial metrics: {e}")
            return None 