# FinBro

A Python client for accessing financial metrics data from FinBro API with satya validation.

## Installation

```bash
pip install finbro
```

## Basic Usage

```python
from finbro import FinbroClient

# Create a client
client = FinbroClient()

# Get financial metrics for a ticker
metrics = client.get_financial_metrics("AAPL")

# Access data
for metric in metrics:
    print(f"{metric.year} Revenue: ${metric.revenue}")
    print(f"{metric.year} Net Income: ${metric.net_income}")
```

## Satya Validation

FinBro uses the satya library for validation, ensuring that all financial data adheres to the expected schema. You can access the schema directly:

```python
from finbro import FinancialMetric
import json

# Get the JSON schema for the FinancialMetric model
schema = FinancialMetric.schema()
print(json.dumps(schema, indent=2))
```

## Available Data

The FinancialMetric model includes:

- ticker: Stock ticker symbol
- year: Financial year
- revenue: Annual revenue
- gross_profit: Gross profit
- operating_income: Operating income
- net_income: Net income
- cash_from_operations: Cash from operations
- cash_from_financing: Cash from financing activities
- cash_from_investing: Cash from investing activities
- capital_expenditure: Capital expenditure
- share_based_comp: Share-based compensation
- total_assets: Total assets
- total_liabilities: Total liabilities
- stockholders_equity: Stockholders' equity
- long_term_debt: Long-term debt
- shares_outstanding: Shares outstanding
- last_updated: Last update timestamp

## Examples

Check out the `examples` directory for more usage examples.

## License

MIT 