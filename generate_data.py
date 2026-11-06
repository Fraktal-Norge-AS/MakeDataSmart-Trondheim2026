#!/usr/bin/env python3
"""
Synthetic financial dataset for "Talk To Your Data" demos.

Company: Nordvidde Group, a Nordic wholesale distributor of outdoor and sports
equipment. HQ in Norway, subsidiaries in Sweden, Denmark, Finland and Germany.

Files:
    config.py             shared settings (period, seed)
    create_company.py     table definitions, one create_<table>(con) per table
    fill_company_data.py  data, one fill_<table>(con) per table
    name_lists.py         company names and word lists
    generate_data.py      entry point: creates the tables, then fills them

Planted data-quality issues are listed in <db>_answer_key.csv, outside the
database, so we can check whether an LLM finds them from the data alone.

Usage:
    pip install duckdb
    python generate_data.py                 # creates nordvidde.duckdb
    python generate_data.py --db demo.duckdb --overwrite
    python generate_data.py --overwrite --parquet        # also writes parquet/<table>.parquet
"""
import argparse
import csv
import os
import time

import duckdb

from create_company import (
    create_entities, create_currencies, create_chart_of_accounts, create_dim_date,
    create_fx_rates, create_customers, create_suppliers, create_products, create_users,
    create_report_definitions, create_report_lines, create_report_line_mapping,
    create_report_line_totals, create_ar_invoices, create_ar_payments, create_ap_invoices,
    create_ap_payments, create_gl_journals, create_gl_lines, create_employees,
    create_payroll_payments, create_sales_orders, create_sales_order_lines,
)
from fill_company_data import (
    fill_entities, fill_currencies, fill_chart_of_accounts, fill_dim_date,
    fill_fx_rates, fill_customers, fill_suppliers, fill_products, fill_users, fill_employees,
    fill_report_definitions, fill_report_lines, fill_report_line_mapping,
    fill_report_line_totals, PLANTED_ISSUES,
)
from fill_ledger import fill_ledger
from rename_layer import apply_norwegian_names, translate_issue, SCHEMA_TRAPS

# (table name, create function, fill function), in dependency order
STEPS = [
    ("entities",          create_entities,          fill_entities),
    ("currencies",        create_currencies,        fill_currencies),
    ("chart_of_accounts", create_chart_of_accounts, fill_chart_of_accounts),
    ("dim_date",          create_dim_date,          fill_dim_date),
    ("fx_rates",          create_fx_rates,          fill_fx_rates),
    ("customers",         create_customers,         fill_customers),
    ("suppliers",         create_suppliers,         fill_suppliers),
    ("products",          create_products,          fill_products),
    ("users",             create_users,             fill_users),
    ("employees",         create_employees,         fill_employees),
    ("report_definitions",  create_report_definitions,  fill_report_definitions),
    ("report_lines",        create_report_lines,        fill_report_lines),
    ("report_line_mapping", create_report_line_mapping, fill_report_line_mapping),
    ("report_line_totals",  create_report_line_totals,  fill_report_line_totals),
    # Transactions: fill_ledger fills all of these at once
    ("ar_invoices",       create_ar_invoices,       fill_ledger),
    ("ar_payments",       create_ar_payments,       None),
    ("ap_invoices",       create_ap_invoices,       None),
    ("ap_payments",       create_ap_payments,       None),
    ("gl_journals",       create_gl_journals,       None),
    ("gl_lines",          create_gl_lines,          None),
    ("payroll_payments",  create_payroll_payments,  None),
    ("sales_orders",      create_sales_orders,      None),
    ("sales_order_lines", create_sales_order_lines, None),
]


def export_parquet(con, folder):
    """One Parquet file per table, e.g. for upload to MotherDuck."""
    os.makedirs(folder, exist_ok=True)
    tables = [r[0] for r in con.execute(
        "SELECT table_name FROM duckdb_tables() WHERE schema_name = 'main' "
        "AND database_name = current_database() ORDER BY table_name").fetchall()]
    print(f"\nParquet export to {folder}/")
    for table in tables:
        t = time.perf_counter()
        path = os.path.join(folder, f"{table}.parquet").replace("\\", "/")
        con.execute(f"COPY (SELECT * FROM main.{table}) TO '{path}' (FORMAT PARQUET)")
        print(f"  {table:<20} {time.perf_counter() - t:6.1f} s")


def main():
    parser = argparse.ArgumentParser(description="Generate Nordvidde demo dataset")
    parser.add_argument("--db", default="nordvidde.duckdb", help="DuckDB file to create")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing file")
    parser.add_argument("--parquet", nargs="?", const="parquet", metavar="DIR",
                        help="Also export every table to DIR/<table>.parquet (default: parquet)")
    args = parser.parse_args()

    if os.path.exists(args.db):
        if not args.overwrite:
            raise SystemExit(f"{args.db} already exists. Use --overwrite to replace it.")
        os.remove(args.db)

    con = duckdb.connect(args.db)

    # One transaction for the whole build, so the file is written once.
    started = time.perf_counter()
    con.begin()
    for _, create, _ in STEPS:
        create(con)
    for name, _, fill in STEPS:
        t = time.perf_counter()
        if fill:
            fill(con)
        count = con.execute(f"SELECT count(*) FROM {name}").fetchone()[0]
        print(f"  {name:<20} {count:>12,} rows  {time.perf_counter() - t:6.1f} s")
    # Last: Norwegian table and column names (the code uses the English ones)
    apply_norwegian_names(con)
    con.commit()
    print(f"  {'total':<20} {'':>12}       {time.perf_counter() - started:6.1f} s")

    if args.parquet:
        export_parquet(con, args.parquet)
    con.close()

    key_path = os.path.splitext(args.db)[0] + "_answer_key.csv"
    with open(key_path, "w", newline="", encoding="utf-8-sig") as f:  # BOM so Excel reads ø/å
        writer = csv.DictWriter(f, fieldnames=["issue_type", "table_name", "record_id",
                                               "related_id", "description"])
        writer.writeheader()
        writer.writerows([translate_issue(i) for i in PLANTED_ISSUES] + SCHEMA_TRAPS)

    print(f"\nDone: {args.db}")
    print(f"Answer key: {key_path} ({len(PLANTED_ISSUES)} planted issues)")


if __name__ == "__main__":
    main()
