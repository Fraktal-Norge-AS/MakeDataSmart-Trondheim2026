# MakeDataSmart-Trondheim2026
# Nordvidde Group: synthetic financial dataset

A generator for a realistic, fairly large financial dataset, made for
"Talk To Your Data" demos where an AI answers questions about the data in
plain language.

**Nordvidde Group** is a fictional Nordic wholesaler of outdoor and sports
equipment: a Norwegian head office and subsidiaries in Sweden, Denmark,
Finland and Germany. The dataset covers January 2023 up to the last full
month and contains:

- master data: customers, suppliers, products, employees, users and a chart of accounts
- about 10 million general ledger lines, with sales and purchase invoices,
  payments, sales orders, payroll and intercompany trading
- six currencies, with daily Norges Bank exchange rates
- report definitions for P&L, balance sheet and a management report

The tables and columns have Norwegian ERP-style names (`kunde`, `hovedbok_linje`,
`bilagsnr` ...), like an older Norwegian accounting system. The data also
contains planted stories and data-quality problems for the AI to find.
They are not described here, so you can test whether an AI finds them.

## Run it

You need Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py --overwrite --parquet
```

This creates `nordvidde.duckdb` and one Parquet file per table in `parquet/`.
The data is reproducible (fixed seed), but the period ends with the last full
month before the day you run it.

Options:

| Option | What it does |
|---|---|
| `--db <file>` | DuckDB file to create (default `nordvidde.duckdb`) |
| `--overwrite` | Replace an existing file |
| `--parquet [folder]` | Also export every table to Parquet (default `parquet/`) |

Exchange rates come from `fx_rates.csv` (Norges Bank). If you run the
generator for months after the last date in it, download a fresh file from
the Norges Bank API and save it as `fx_rates.csv`:

<https://data.norges-bank.no/api/data/EXR/B.USD+EUR+GBP+SEK+DKK.NOK.SP?format=csv&startPeriod=2023-01-01&locale=en>

## Star schema (optional)

`DatamartQueries/` holds views that turn the source tables into a star
schema with English names (`Dim_Customer`, `Fact_GeneralLedger`,
`Fact_Subledger` ...), including a bridge-based report setup for Power BI.
They are written for MotherDuck and expect:

- the source tables in `MakeDataSmart2026.mds` (e.g. loaded from the Parquet files)
- an empty schema `MakeDataSmart2026.mds_datamart` for the views

Create the dimensions first, then the facts and bridges.

## Project layout

| File | Purpose |
|---|---|
| `generate_data.py` | Entry point |
| `config.py` | Period, seed and other settings |
| `create_company.py` | Table definitions |
| `fill_company_data.py` | Master data |
| `fill_ledger.py` | Transactions: sales, purchases, payments, payroll, ledger |
| `stories.py`, `name_lists.py` | Planted stories, company names and word lists |
| `rename_layer.py` | Renames everything to Norwegian at the end |

## License

See [LICENSE](LICENSE).
