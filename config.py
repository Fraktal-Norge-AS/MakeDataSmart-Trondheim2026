"""Shared configuration for the Nordvidde Group dataset."""
import os
from datetime import date, timedelta

START_DATE = date(2023, 1, 1)
# Last day of the previous month, so the current year is partial and the data
# supports questions like "give me a prognosis for this year using last year".
# Note: the output therefore changes with the month the script is run in.
END_DATE = date.today().replace(day=1) - timedelta(days=1)
SEED = 42                       # used for reproducible data

# Master data sizes
CUSTOMERS_PER_ENTITY = {"NO01": 820, "SE01": 650, "DK01": 350, "FI01": 300, "DE01": 380}
SMALL_BRAND_SUPPLIERS = 40      # generated goods suppliers, on top of the handwritten ones
SERVICE_SUPPLIERS_PER_ENTITY = {"NO01": 35, "SE01": 25, "DK01": 15, "FI01": 13, "DE01": 17}
N_PRODUCTS = 2000

# Employees at the start of the period (incl. the ERP users), and the yearly
# pay rise applied every 1 April from 2023
HEADCOUNT = {"NO01": 280, "SE01": 200, "DK01": 100, "FI01": 80, "DE01": 120}
SALARY_RAISE = 0.035

# Roger Bakke's bank accounts (stories): his salary account, and the account
# his second salary payment goes to. Shell suppliers are paid to these too.
ROGER_SALARY_ACCOUNT = "NO24 6147 8805 804"
ROGER_SECOND_ACCOUNT = "NO62 9710 0513 842"

# Planted data-quality issues: the same company entered twice with different IDs
DUPLICATE_CUSTOMERS = 20
DUPLICATE_SUPPLIERS = 8

# Daily Norges Bank rates (semicolon-separated SDMX CSV, SEK/DKK per 100 units)
FX_RATES_FILE = os.path.join(os.path.dirname(__file__), "fx_rates.csv")

# Rough rates, only used to set plausible prices and credit limits in master
# data. The real FX rates are supplied later and used for the ledger.
APPROX_FX_TO_NOK = {"NOK": 1.0, "SEK": 0.98, "DKK": 1.55, "EUR": 11.6, "USD": 10.7, "GBP": 13.5}
