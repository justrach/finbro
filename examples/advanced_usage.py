"""
FinBro Advanced Usage Example with Satya Validation

This example demonstrates more advanced features of FinBro library
with Satya validation, including:
- Stream validation
- Schema generation
- Type information
- Custom validation workflows
"""

import json
from finbro import FinbroClient, FinancialMetric
from typing import List, Dict, Any


def print_json(data):
    """Helper to print JSON data nicely"""
    print(json.dumps(data, indent=2))


def generate_mock_data() -> List[Dict[str, Any]]:
    """Generate sample financial data for demonstration purposes.
    Some of this data will be valid, some invalid.
    """
    return [
        {
            # Valid entry
            "ticker": "MSFT",
            "year": 2021,
            "revenue": 168088000000,
            "gross_profit": 115856000000,
            "operating_income": 69916000000,
            "net_income": 61271000000,
            "cash_from_operations": 76740000000,
            "cash_from_financing": -38704000000,
            "cash_from_investing": -30311000000,
            "capital_expenditure": -20716000000,
            "share_based_comp": 6118000000,
            "total_assets": 333779000000,
            "total_liabilities": 192266000000,
            "stockholders_equity": 141513000000,
            "long_term_debt": 50074000000,
            "shares_outstanding": 7547000000,
            "last_updated": "2023-01-15"
        },
        {
            # Invalid: year as a string
            "ticker": "GOOG",
            "year": "2021",  # Invalid - should be int
            "revenue": 257637000000,
            "gross_profit": 144896000000,
            "operating_income": 78714000000,
            "net_income": 76033000000,
            "cash_from_operations": 91652000000,
            "cash_from_financing": -61376000000,
            "cash_from_investing": -26992000000,
            "capital_expenditure": -24640000000,
            "share_based_comp": 15703000000,
            "total_assets": 359268000000,
            "total_liabilities": 97531000000,
            "stockholders_equity": 251737000000,
            "long_term_debt": 14817000000,
            "shares_outstanding": 13244000000,
            "last_updated": "2023-01-15"
        },
        {
            # Invalid: missing required field (operating_income)
            "ticker": "AMZN",
            "year": 2021,
            "revenue": 469822000000,
            "gross_profit": 197478000000,
            # missing operating_income
            "net_income": 33364000000,
            "cash_from_operations": 46327000000,
            "cash_from_financing": -26573000000,
            "cash_from_investing": -29991000000,
            "capital_expenditure": -55396000000,
            "share_based_comp": 12757000000,
            "total_assets": 420549000000,
            "total_liabilities": 282304000000,
            "stockholders_equity": 138245000000,
            "long_term_debt": 67651000000,
            "shares_outstanding": 10078000000,
            "last_updated": "2023-01-15"
        }
    ]


def log_validation_error(ticker: str, errors: List[str]):
    """Log validation errors for a ticker"""
    print(f"\n❌ Validation failed for {ticker}:")
    for error in errors:
        print(f"  - {error}")


def process_valid_metric(metric: FinancialMetric):
    """Process a valid financial metric"""
    print(f"\n✅ Valid metric for {metric.ticker} ({metric.year}):")
    print(f"  - Revenue: ${metric.revenue:,.0f}")
    print(f"  - Net Income: ${metric.net_income:,.0f}")
    print(f"  - Operating Margin: {(metric.operating_income / metric.revenue * 100):.2f}%")
    print(f"  - Return on Equity: {(metric.net_income / metric.stockholders_equity * 100):.2f}%")


def main():
    # Create a validator from the FinancialMetric model
    validator = FinancialMetric.validator()
    
    # Get the JSON schema for the FinancialMetric model
    schema = validator.model_schema()
    print("📊 FinancialMetric JSON Schema:")
    print_json(schema)
    
    # Get type information
    type_info = validator.get_type_info("FinancialMetric")
    print("\n📝 FinancialMetric Type Information:")
    print(f"Documentation: {type_info['doc']}")
    print("Fields:")
    for field_name, field_info in type_info['fields'].items():
        print(f"  - {field_name}: {field_info['type']} ({field_info['description']})")
    
    # Generate mock data for demonstration
    mock_data = generate_mock_data()
    print(f"\n🔄 Validating {len(mock_data)} mock financial records...")
    
    # Validate the mock data stream
    valid_count = 0
    for result in validator.validate_stream(mock_data, collect_errors=True):
        if result.is_valid:
            metric = FinancialMetric(**result.value)
            process_valid_metric(metric)
            valid_count += 1
        else:
            # Get the ticker from the original data if possible
            ticker = result.value.get("ticker", "UNKNOWN") if result.value else "UNKNOWN"
            log_validation_error(ticker, result.errors)
    
    print(f"\n🔍 Validation Summary: {valid_count} valid out of {len(mock_data)} records")
    
    # Example with real API call
    print("\n🌐 Fetching live data from FinBro API...")
    client = FinbroClient()
    try:
        metrics = client.get_financial_metrics("AAPL")
        if metrics and len(metrics) > 0:
            print(f"Retrieved {len(metrics)} years of financial data for AAPL")
            latest = sorted(metrics, key=lambda x: x.year)[-1]
            print(f"Latest year: {latest.year}")
            print(f"Revenue: ${latest.revenue:,.0f}")
            print(f"Net Income: ${latest.net_income:,.0f}")
        else:
            print("No valid metrics found for AAPL")
    except Exception as e:
        print(f"Error fetching real data: {e}")


if __name__ == "__main__":
    main() 