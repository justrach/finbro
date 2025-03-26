"""
FinBro Basic Usage Example

This example shows how to use the FinBro client to fetch financial metrics for
a company and work with the validated data.
"""

import json
from finbro import FinbroClient, FinancialMetric


def print_json(data):
    """Helper to print JSON data nicely"""
    print(json.dumps(data, indent=2))


def calculate_growth_rates(metrics):
    """Calculate year-over-year growth rates for key metrics"""
    if len(metrics) < 2:
        print("Need at least two years of data to calculate growth rates")
        return {}
    
    growth_rates = []
    
    # Sort by year to ensure proper calculation
    sorted_metrics = sorted(metrics, key=lambda x: x.year)
    
    for i in range(1, len(sorted_metrics)):
        current = sorted_metrics[i]
        previous = sorted_metrics[i-1]
        
        # Skip if previous year has zero values to avoid division by zero
        if previous.revenue == 0:
            continue
            
        growth = {
            "ticker": current.ticker,
            "year": current.year,
            "revenue_growth": (current.revenue - previous.revenue) / previous.revenue * 100,
            "net_income_growth": (current.net_income - previous.net_income) / previous.net_income * 100 if previous.net_income != 0 else None,
            "gross_margin": current.gross_profit / current.revenue * 100 if current.revenue != 0 else None,
            "operating_margin": current.operating_income / current.revenue * 100 if current.revenue != 0 else None,
            "net_margin": current.net_income / current.revenue * 100 if current.revenue != 0 else None,
        }
        
        growth_rates.append(growth)
    
    return growth_rates


def main():
    # Create a client instance
    client = FinbroClient()
    
    # Create a validator for manual validation example
    validator = FinancialMetric.validator()
    
    # Example of manual validation
    sample_data = {
        "ticker": "AAPL",
        "year": 2022,
        "revenue": 394328000000,
        "gross_profit": 170782000000,
        "operating_income": 119437000000,
        "net_income": 99803000000,
        "cash_from_operations": 122151000000,
        "cash_from_financing": -110749000000,
        "cash_from_investing": -22354000000,
        "capital_expenditure": -10708000000,
        "share_based_comp": 9038000000,
        "total_assets": 352755000000,
        "total_liabilities": 302083000000,
        "stockholders_equity": 50672000000,
        "long_term_debt": 98959000000,
        "shares_outstanding": 15943000000,
        "last_updated": "2023-01-01"
    }
    
    # Validate the data
    print("Validating sample data...")
    result = validator.validate(sample_data)
    if result.is_valid:
        # Create metric from validated data
        metric = FinancialMetric(**result.value)
        print(f"✅ Validation successful for {metric.ticker}")
    else:
        print("❌ Validation failed with errors:", result.errors)
    
    # Get financial metrics for Apple
    print("\nFetching financial metrics for Apple (AAPL)...")
    apple_metrics = client.get_financial_metrics("AAPL")
    
    if not apple_metrics:
        print("Failed to fetch metrics for AAPL")
        return
    
    # Print the number of years we have data for
    print(f"Retrieved data for {len(apple_metrics)} years")
    
    # Show the JSON schema of the FinancialMetric model
    print("\nFinancialMetric JSON Schema:")
    print_json(validator.model_schema())
    
    # Print the most recent year's data
    most_recent = sorted(apple_metrics, key=lambda x: x.year)[-1]
    print(f"\nMost recent data ({most_recent.year}):")
    print(f"Revenue: ${most_recent.revenue:,.0f}")
    print(f"Net Income: ${most_recent.net_income:,.0f}")
    print(f"Operating Income: ${most_recent.operating_income:,.0f}")
    print(f"Cash from Operations: ${most_recent.cash_from_operations:,.0f}")
    
    # Calculate and print growth rates
    print("\nCalculating growth rates...")
    growth_rates = calculate_growth_rates(apple_metrics)
    
    for rate in growth_rates:
        print(f"\nGrowth rates for {rate['year']}:")
        print(f"Revenue growth: {rate['revenue_growth']:.2f}%")
        if rate['net_income_growth'] is not None:
            print(f"Net income growth: {rate['net_income_growth']:.2f}%")
        if rate['gross_margin'] is not None:
            print(f"Gross margin: {rate['gross_margin']:.2f}%")
        if rate['operating_margin'] is not None:
            print(f"Operating margin: {rate['operating_margin']:.2f}%")
        if rate['net_margin'] is not None:
            print(f"Net margin: {rate['net_margin']:.2f}%")


if __name__ == "__main__":
    main() 