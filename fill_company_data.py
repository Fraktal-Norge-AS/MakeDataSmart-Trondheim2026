"""
Data for the Nordvidde Group dataset: one fill_<table>(con) per table.

Assumes the tables already exist (see create_company.py).
"""
import random
from datetime import date, timedelta

import pyarrow as pa

from config import (
    START_DATE, END_DATE, SEED, CUSTOMERS_PER_ENTITY, SMALL_BRAND_SUPPLIERS,
    SERVICE_SUPPLIERS_PER_ENTITY, N_PRODUCTS, APPROX_FX_TO_NOK,
    DUPLICATE_CUSTOMERS, DUPLICATE_SUPPLIERS, FX_RATES_FILE, HEADCOUNT, SALARY_RAISE,
    ROGER_SALARY_ACCOUNT, ROGER_SECOND_ACCOUNT,
)
from name_lists import (
    LOCALE, LEGAL_SUFFIX, FIRST_NAMES, SMALL_BRAND_WORDS, PUN_CUSTOMERS, EXPORT_CUSTOMERS,
    PRODUCT_ITEMS, CATEGORY_MARGIN, PRIVATE_LABEL_EXTRA_MARGIN, MODEL_NAMES,
    MODEL_VARIANTS, PUN_GOODS_SUPPLIERS, PUN_SERVICE_SUPPLIERS,
    SERVICE_CATEGORY_ACCOUNT, SERVICE_CATEGORY_WEIGHT, USERS, SYSTEM_USERS,
    HANDPICKED_DUPLICATES, SHELL_SUPPLIERS,
)

# Customers and products that are new during the period start no later than
# this, and products are discontinued no later than DISCONTINUE_UNTIL. Fixed
# dates, not END_DATE: otherwise these dates shift with the run month, and
# with them every random draw in the ledger.
LAST_NEW_DATE = date(2026, 6, 30)
DISCONTINUE_UNTIL = date(2026, 9, 30)

# Answer key: every planted issue is recorded here and written to a CSV file
# outside the database by generate_data.py. Nothing in the database marks them.
PLANTED_ISSUES = []


def record_issue(issue_type, table_name, record_id, related_id, description):
    PLANTED_ISSUES.append(dict(issue_type=issue_type, table_name=table_name, record_id=record_id,
                               related_id=related_id, description=description))


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def insert_rows(con, table, rows):
    """Insert all rows in one go via Arrow. Columns are matched by position.
    (executemany takes about 10 ms per row in DuckDB.)"""
    data = pa.table({f"c{i}": list(col) for i, col in enumerate(zip(*rows))})
    con.execute(f"INSERT INTO {table} SELECT * FROM data")


def random_date(rng, start, end):
    # Exactly one draw per call, whatever the range. (randint consumes a varying
    # amount of randomness, so a different END_DATE would shift every later pick.)
    return start + timedelta(days=int(rng.random() * ((end - start).days + 1)))


def pick_city(rng, cities):
    """Earlier cities in the list are bigger, so they are picked more often."""
    return rng.choices(cities, weights=[1 / (i + 1) ** 0.7 for i in range(len(cities))])[0]


def fill_template(rng, template, loc):
    """Fill a name template from a locale. Returns (name, city)."""
    surname, surname2 = rng.sample(loc["surnames"], 2)
    nature = rng.choice(loc["nature"])
    city = pick_city(rng, loc["cities"])
    name = template.format(city=city, surname=surname, surname2=surname2,
                           nature=nature, nature_lc=nature.lower(), gear=rng.choice(loc["gear"]))
    return name, city


def unique_name(rng, used, make):
    """Call make() until it returns a name not already in used.
    make() returns a name, or a tuple whose first element is the name."""
    for _ in range(1000):
        result = make()
        name = result[0] if isinstance(result, tuple) else result
        if name not in used:
            used.add(name)
            return result
    raise RuntimeError("Could not generate a unique name")


def price_point(x):
    """Round to a retail-looking price: 349, 2499, 24999."""
    step = 10 if x < 1000 else 50 if x < 10000 else 500
    return max(step, round(x / step) * step) - 1


ITEM_INFO = {item: (category, lo, hi, season)
             for category, items in PRODUCT_ITEMS.items()
             for item, lo, hi, season in items}


def resolve_items(scope):
    """Turn a list of categories and/or product types into product types."""
    items = []
    for s in scope:
        items += [i[0] for i in PRODUCT_ITEMS[s]] if s in PRODUCT_ITEMS else [s]
    return items


# --------------------------------------------------------------------------
# Duplicate companies (planted data-quality issue)
# --------------------------------------------------------------------------
ASCII_MAP = str.maketrans({"æ": "ae", "ø": "o", "å": "a", "ä": "a", "ö": "o", "ü": "u", "é": "e",
                           "Æ": "Ae", "Ø": "O", "Å": "A", "Ä": "A", "Ö": "O", "Ü": "U"})
ALT_LEGAL_FORM = {"AS": "A/S", "A/S": "AS", "ASA": "AS", "AB": "Aktiebolag", "ApS": "Aps",
                  "Oy": "OY", "Oyj": "Oy", "GmbH": "G.m.b.H.", "AG": "A.G.", "SE": "S.E.",
                  "SA": "S.A.", "SAS": "S.A.S.", "BV": "B.V.", "Ltd": "Limited", "Ltd.": "Limited",
                  "Inc": "Inc.", "Inc.": "Inc"}
AND_WORD = {"NO": "og", "SE": "och", "DK": "og", "FI": "ja", "DE": "und"}


def duplicate_name(rng, name, country):
    """A sloppy re-entry of a company name. Returns (variation, new name)."""
    words = name.split(" ")
    variants = [("upper case", name.upper()),
                ("extra space", name.replace(" ", "  ", 1))]
    if len(words) > 1 and words[-1] in ALT_LEGAL_FORM:
        variants.append(("legal form missing", " ".join(words[:-1])))
        variants.append(("different legal form", " ".join(words[:-1] + [ALT_LEGAL_FORM[words[-1]]])))
    if name.translate(ASCII_MAP) != name:
        variants.append(("Nordic letters replaced", name.translate(ASCII_MAP)))
    if " & " in name:
        variants.append(("'&' written out", name.replace(" & ", f" {AND_WORD.get(country, 'and')} ")))
    swappable = [i for i in range(1, len(name) - 1)
                 if name[i].isalpha() and name[i + 1].isalpha() and name[i] != name[i + 1]]
    if swappable:
        i = rng.choice(swappable)
        variants.append(("typo", name[:i] + name[i + 1] + name[i] + name[i + 2:]))
    return rng.choice(variants)


def plant_duplicates(rng, rows, candidates, n, used, prefix, width, country_col,
                     label, table, mutate):
    """Append n duplicates of randomly chosen candidates, with new IDs at the end
    (created later, by mistake). A few originals are entered three times in total.
    Rows are [id, name, ...]; mutate(dup, variation) changes other fields."""
    originals = rng.sample(candidates, n - n // 5)
    next_id = len(rows) + 1
    for orig in originals + originals[: n // 5]:
        for _ in range(10):
            variation, name = duplicate_name(rng, orig[1], orig[country_col])
            if name not in used:
                break
        else:
            continue
        used.add(name)
        dup = list(orig)
        dup[0], dup[1] = f"{prefix}{next_id:0{width}d}", name
        next_id += 1
        mutate(dup, variation)
        rows.append(dup)
        record_issue(f"Duplicate {label}", table, dup[0], orig[0],
                     f"'{name}' is the same company as '{orig[1]}' ({variation})")


# --------------------------------------------------------------------------
# Base tables
# --------------------------------------------------------------------------
def fill_entities(con):
    con.execute("""
        INSERT INTO entities VALUES
        ('NO01', 'Nordvidde Outdoor AS',      'NO', 'Norway',  'Oslo',       'NOK', TRUE),
        ('SE01', 'Nordvidde Sverige AB',      'SE', 'Sweden',  'Gothenburg', 'SEK', FALSE),
        ('DK01', 'Nordvidde Danmark ApS',     'DK', 'Denmark', 'Aarhus',     'DKK', FALSE),
        ('FI01', 'Nordvidde Suomi Oy',        'FI', 'Finland', 'Tampere',    'EUR', FALSE),
        ('DE01', 'Nordvidde Deutschland GmbH','DE', 'Germany', 'Hamburg',    'EUR', FALSE)
    """)


def fill_currencies(con):
    con.execute("""
        INSERT INTO currencies VALUES
        ('NOK', 'Norwegian krone'),
        ('SEK', 'Swedish krona'),
        ('DKK', 'Danish krone'),
        ('EUR', 'Euro'),
        ('USD', 'US dollar'),
        ('GBP', 'British pound')
    """)


def fill_chart_of_accounts(con):
    accounts = [
        # Assets
        (1200, 'Machinery and equipment',        'Asset',     'Fixed assets',           'BS'),
        (1230, 'Vehicles',                       'Asset',     'Fixed assets',           'BS'),
        (1460, 'Inventory',                      'Asset',     'Inventory',              'BS'),
        (1500, 'Accounts receivable',            'Asset',     'Receivables',            'BS'),
        (1560, 'Intercompany receivables',       'Asset',     'Receivables',            'BS'),
        (1920, 'Bank',                           'Asset',     'Cash and bank',          'BS'),
        # Equity and liabilities
        (2000, 'Share capital',                  'Equity',    'Equity',                 'BS'),
        (2050, 'Retained earnings',              'Equity',    'Equity',                 'BS'),
        (2220, 'Bank loan',                      'Liability', 'Long-term liabilities',  'BS'),
        (2400, 'Accounts payable',               'Liability', 'Payables',               'BS'),
        (2500, 'Tax payable',                    'Liability', 'Public duties',          'BS'),
        (2460, 'Intercompany payables',          'Liability', 'Payables',               'BS'),
        (2600, 'Withholding tax',                'Liability', 'Public duties',          'BS'),
        (2700, 'Output VAT',                     'Liability', 'Public duties',          'BS'),
        (2710, 'Input VAT',                      'Liability', 'Public duties',          'BS'),
        (2770, 'Employer social security',       'Liability', 'Public duties',          'BS'),
        (2950, 'Unidentified payments (suspense)', 'Liability', 'Payables',             'BS'),
        # Revenue
        (3000, 'Sales revenue, domestic',        'Revenue',   'Revenue',                'PL'),
        (3100, 'Sales revenue, export',          'Revenue',   'Revenue',                'PL'),
        (3200, 'Sales revenue, online',          'Revenue',   'Revenue',                'PL'),
        (3400, 'Sales revenue, intercompany',    'Revenue',   'Revenue',                'PL'),
        (3700, 'Freight income',                 'Revenue',   'Revenue',                'PL'),
        (3900, 'Other operating income',         'Revenue',   'Revenue',                'PL'),
        (3910, 'Management fee, intercompany',   'Revenue',   'Revenue',                'PL'),
        # Cost of goods sold
        (4000, 'Purchase of goods for resale',   'Expense',   'Cost of goods sold',     'PL'),
        (4060, 'Freight on purchases',           'Expense',   'Cost of goods sold',     'PL'),
        (4090, 'Inventory change',               'Expense',   'Cost of goods sold',     'PL'),
        (4300, 'Cost of goods sold, intercompany', 'Expense', 'Cost of goods sold',     'PL'),
        # Payroll
        (5000, 'Salaries',                       'Expense',   'Payroll',                'PL'),
        (5090, 'Bonuses and commissions',        'Expense',   'Payroll',                'PL'),
        (5400, 'Employer social security',       'Expense',   'Payroll',                'PL'),
        (5900, 'Other personnel costs',          'Expense',   'Payroll',                'PL'),
        # Other operating expenses
        (6000, 'Depreciation',                   'Expense',   'Depreciation',           'PL'),
        (6300, 'Rent, premises',                 'Expense',   'Other operating costs',  'PL'),
        (6340, 'Electricity and heating',        'Expense',   'Other operating costs',  'PL'),
        (6360, 'Cleaning and facility services', 'Expense',   'Other operating costs',  'PL'),
        (6540, 'Equipment and furniture',        'Expense',   'Other operating costs',  'PL'),
        (6700, 'Consulting and audit fees',      'Expense',   'Other operating costs',  'PL'),
        (6790, 'Management fee, intercompany',   'Expense',   'Other operating costs',  'PL'),
        (6800, 'Office supplies',                'Expense',   'Other operating costs',  'PL'),
        (6900, 'Telephone and internet',         'Expense',   'Other operating costs',  'PL'),
        (7100, 'Vehicle costs',                  'Expense',   'Other operating costs',  'PL'),
        (7140, 'Travel expenses',                'Expense',   'Other operating costs',  'PL'),
        (7300, 'Marketing and advertising',      'Expense',   'Sales and marketing',    'PL'),
        (7320, 'Trade fairs and events',         'Expense',   'Sales and marketing',    'PL'),
        (7500, 'Insurance',                      'Expense',   'Other operating costs',  'PL'),
        (7770, 'Bank charges',                   'Expense',   'Other operating costs',  'PL'),
        (7830, 'Bad debt losses',                'Expense',   'Other operating costs',  'PL'),
        # Financial items
        (8050, 'Interest income',                'Revenue',   'Financial items',        'PL'),
        (8060, 'Currency gains (agio)',          'Revenue',   'Financial items',        'PL'),
        (8150, 'Interest expense',               'Expense',   'Financial items',        'PL'),
        (8160, 'Currency losses (disagio)',      'Expense',   'Financial items',        'PL'),
        (8300, 'Income tax',                     'Expense',   'Tax',                    'PL'),
    ]
    insert_rows(con, "chart_of_accounts", accounts)


def fill_dim_date(con):
    """One row per day for the full period, generated directly in DuckDB."""
    con.execute(f"""
        INSERT INTO dim_date
        SELECT
            d::DATE,
            year(d),
            quarter(d),
            month(d),
            strftime(d, '%B'),
            strftime(d, '%Y-%m'),
            weekofyear(d),
            isodow(d),
            strftime(d, '%A'),
            isodow(d) IN (6, 7)
        FROM range(DATE '{START_DATE}', DATE '{END_DATE}' + INTERVAL 1 DAY, INTERVAL 1 DAY) t(d)
    """)


def fill_fx_rates(con):
    """Norges Bank rates for each day in dim_date. Days without a rate take the
    previous business day's; days before the first rate take the first one."""
    path = FX_RATES_FILE.replace("\\", "/")
    con.execute(f"""
        INSERT INTO fx_rates
        WITH raw AS (
            SELECT BASE_CUR AS currency_code, TIME_PERIOD AS source_date,
                   OBS_VALUE / 10 ^ UNIT_MULT AS rate
            FROM read_csv('{path}', delim = ';')
        ),
        first_rate AS (
            SELECT currency_code, arg_min(rate, source_date) AS rate,
                   min(source_date) AS source_date
            FROM raw GROUP BY ALL
        )
        SELECT d.date, f.currency_code,
               coalesce(r.rate, f.rate), coalesce(r.source_date, f.source_date)
        FROM dim_date d
        CROSS JOIN first_rate f
        ASOF LEFT JOIN raw r ON r.currency_code = f.currency_code AND d.date >= r.source_date
        UNION ALL
        SELECT date, 'NOK', 1, date FROM dim_date
    """)


# --------------------------------------------------------------------------
# Report setup
# --------------------------------------------------------------------------
# Each line: (line_id, line_name, line_type, sign, spec).
# mapped: spec is a list of (account_from, account_to, entity_id, product_category)
# total:  spec is a list of component line_ids
def _mapped(line_id, name, ranges, sign=-1):
    return (line_id, name, "mapped", sign, [r + (None,) * (4 - len(r)) for r in ranges])


def _total(line_id, name, components):
    return (line_id, name, "total", None, components)


def _header(line_id, name):
    return (line_id, name, "header", None, [])


PL_LINES = [
    _header("H_OP",    "Operating income and expenses"),
    _mapped("REV",     "Revenue",                     [(3000, 3999)]),
    _mapped("COGS",    "Cost of goods sold",          [(4000, 4999)]),
    _total("GM",       "Gross margin",                ["REV", "COGS"]),
    _mapped("PAY",     "Payroll",                     [(5000, 5999)]),
    # Planted issue: set up when only 6300 and 6340 existed, so 6360 is missed.
    _mapped("PREM",    "Premises",                    [(6300, 6350)]),
    _mapped("OFFICE",  "Office, IT and consulting",   [(6500, 6999)]),
    _mapped("TRAVEL",  "Vehicles and travel",         [(7000, 7199)]),
    _mapped("MKT",     "Sales and marketing",         [(7300, 7399)]),
    _mapped("OTHER",   "Other operating costs",       [(7400, 7999)]),
    _total("OPEX",     "Total operating expenses",    ["PAY", "PREM", "OFFICE", "TRAVEL", "MKT", "OTHER"]),
    _total("EBITDA",   "EBITDA",                      ["GM", "OPEX"]),
    _mapped("DEP",     "Depreciation",                [(6000, 6099)]),
    _total("EBIT",     "Operating result (EBIT)",     ["EBITDA", "DEP"]),
    _mapped("FIN",     "Net financial items",         [(8000, 8299)]),
    _total("EBT",      "Result before tax",           ["EBIT", "FIN"]),
    _mapped("TAX",     "Income tax",                  [(8300, 8399)]),
    _total("NET",      "Net result",                  ["EBT", "TAX"]),
]

BS_LINES = [
    _header("H_ASSETS", "Assets"),
    _mapped("FIXED",  "Fixed assets",                 [(1000, 1399)], sign=1),
    _mapped("INV",    "Inventory",                    [(1400, 1499)], sign=1),
    _mapped("REC",    "Receivables",                  [(1500, 1899)], sign=1),
    _mapped("CASH",   "Cash and bank",                [(1900, 1999)], sign=1),
    _total("TA",      "Total assets",                 ["FIXED", "INV", "REC", "CASH"]),
    _header("H_EQL",  "Equity and liabilities"),
    _mapped("EQUITY", "Paid-in and retained equity",  [(2000, 2099)]),
    _mapped("RESULT", "Result for the period",        [(3000, 8999)]),
    _total("TEQ",     "Total equity",                 ["EQUITY", "RESULT"]),
    _mapped("LTL",    "Long-term liabilities",        [(2100, 2299)]),
    _mapped("STL",    "Short-term liabilities",       [(2300, 2999)]),
    _total("TL",      "Total liabilities",            ["LTL", "STL"]),
    _total("TEL",     "Total equity and liabilities", ["TEQ", "TL"]),
]


def _mgmt_lines():
    """Management P&L: account x product category, plus a memo by account x entity."""
    cats = {c.split()[0].upper()[:4]: c for c in CATEGORY_MARGIN}
    nordic = ["NO01", "SE01", "DK01", "FI01"]
    return (
        [_header("H_REV", "Revenue by product area")]
        + [_mapped(f"REV_{k}", f"Revenue – {c}", [(3000, 3299, None, c)]) for k, c in cats.items()]
        + [_mapped("REV_OTHER", "Freight and other income", [(3300, 3999)]),
           _total("REV", "Total revenue", [f"REV_{k}" for k in cats] + ["REV_OTHER"]),
           _header("H_COGS", "Cost of goods sold by product area")]
        + [_mapped(f"COGS_{k}", f"COGS – {c}", [(4000, 4059, None, c)]) for k, c in cats.items()]
        + [_mapped("COGS_OTHER", "Freight and inventory change", [(4060, 4999)]),
           _total("COGS", "Total cost of goods sold", [f"COGS_{k}" for k in cats] + ["COGS_OTHER"]),
           _header("H_GM", "Gross margin by product area")]
        + [_total(f"GM_{k}", f"Gross margin – {c}", [f"REV_{k}", f"COGS_{k}"]) for k, c in cats.items()]
        + [_total("GM_OTHER", "Gross margin – other", ["REV_OTHER", "COGS_OTHER"]),
           _total("GM", "Total gross margin", [f"GM_{k}" for k in cats] + ["GM_OTHER"]),
           _mapped("OPEX", "Operating expenses excl. depreciation", [(5000, 5999), (6100, 7999)]),
           _total("EBITDA", "EBITDA", ["GM", "OPEX"]),
           _header("H_REGION", "Memo: revenue by region"),
           _mapped("REG_NORDIC", "Revenue – Nordic entities", [(3000, 3999, e) for e in nordic]),
           _mapped("REG_DE", "Revenue – Germany", [(3000, 3999, "DE01")]),
           _total("REG_TOTAL", "Total revenue by region", ["REG_NORDIC", "REG_DE"])]
    )


REPORTS = [
    ("PL",   "Profit and loss",  "Statutory-style P&L with EBITDA and EBIT", PL_LINES),
    ("BS",   "Balance sheet",    "Assets, equity and liabilities", BS_LINES),
    ("MGMT", "Management P&L",   "Revenue, COGS and gross margin by product area; "
                                 "revenue by region", _mgmt_lines()),
]


def fill_report_definitions(con):
    insert_rows(con, "report_definitions", [r[:3] for r in REPORTS])


def fill_report_lines(con):
    rows = [(report_id, line_id, name, (i + 1) * 10, line_type, sign)
            for report_id, _, _, lines in REPORTS
            for i, (line_id, name, line_type, sign, _) in enumerate(lines)]
    insert_rows(con, "report_lines", rows)


def fill_report_line_mapping(con):
    rows = [(report_id, line_id) + r
            for report_id, _, _, lines in REPORTS
            for line_id, _, line_type, _, spec in lines if line_type == "mapped"
            for r in spec]
    insert_rows(con, "report_line_mapping", [(i,) + r for i, r in enumerate(rows, 1)])
    record_issue("Report mapping gap", "report_line_mapping", "PL", "6360",
                 "Account 6360 (Cleaning and facility services) is not mapped in report PL: "
                 "line PREM covers 6300-6350 only. PL EBITDA is overstated and differs from MGMT EBITDA")


def fill_report_line_totals(con):
    rows = [(report_id, line_id, c)
            for report_id, _, _, lines in REPORTS
            for line_id, _, line_type, _, spec in lines if line_type == "total"
            for c in spec]
    insert_rows(con, "report_line_totals", rows)


# --------------------------------------------------------------------------
# Master data
# --------------------------------------------------------------------------
CUSTOMER_TERMS = {
    "Key account": [60], "Chain store": [45, 60], "Independent": [14, 30, 30, 30],
    "Webshop": [30], "Online consumers": [0],
}
CUSTOMER_CREDIT_NOK = {
    "Key account": (40e6, 80e6), "Chain store": (10e6, 25e6), "Independent": (50e3, 500e3),
    "Webshop": (200e3, 2e6), "Online consumers": (0, 0),
}


def fill_customers(con):
    """Handwritten parody customers plus a generated long tail per entity."""
    rng = random.Random(f"{SEED}-customers")
    entities = {e: (country, currency) for e, country, currency in
                con.execute("SELECT entity_id, country_code, currency_code FROM entities").fetchall()}
    rows, used = [], set()

    def add(name, entity_id, segment, country, city, currency, since, terms=None):
        lo, hi = CUSTOMER_CREDIT_NOK[segment]
        credit = round(rng.uniform(lo, hi) / APPROX_FX_TO_NOK[currency], -3)
        rows.append([name, entity_id, segment, country, city, currency,
                     terms if terms is not None else rng.choice(CUSTOMER_TERMS[segment]),
                     credit, since])
        used.add(name)

    def since_date(since):
        if isinstance(since, tuple):
            return date(*since)
        return random_date(rng, date(since, 1, 1), date(since, 12, 31))

    for entity_id, name, segment, city, since in PUN_CUSTOMERS:
        country, currency = entities[entity_id]
        add(name, entity_id, segment, country, city, currency, since_date(since))
    for name, segment, country, city, currency, since in EXPORT_CUSTOMERS:
        add(name, "NO01", segment, country, city, currency, since_date(since),
            terms=rng.choice([30, 45]))

    # Generated long tail. About a quarter are new during the period (growth).
    for entity_id, target in CUSTOMERS_PER_ENTITY.items():
        country, currency = entities[entity_id]
        loc = LOCALE[country]
        n = target - sum(1 for r in rows if r[1] == entity_id)
        for _ in range(n):
            segment = "Webshop" if rng.random() < 0.08 else "Independent"
            templates = loc["webshop"] if segment == "Webshop" else loc["retail"]
            name, city = unique_name(rng, used, lambda: fill_template(rng, rng.choice(templates), loc))
            if rng.random() < 0.75:
                since = random_date(rng, date(2000, 1, 1), START_DATE - timedelta(days=1))
            else:
                since = random_date(rng, START_DATE, LAST_NEW_DATE)
            add(name, entity_id, segment, country, city, currency, since)

    rng.shuffle(rows)  # so customer IDs don't reveal which ones are handwritten
    rows = [[f"C{i:05d}"] + r for i, r in enumerate(rows, 1)]

    # Row layout: id, name, entity, segment, country, city, currency, terms, credit, since
    def mutate(dup, variation):
        if variation == "Nordic letters replaced":
            dup[5] = dup[5].translate(ASCII_MAP)
        dup[9] = random_date(rng, max(dup[9], START_DATE), LAST_NEW_DATE)
        if rng.random() < 0.5:
            dup[7] = rng.choice(CUSTOMER_TERMS[dup[3]])
        if rng.random() < 0.5:
            dup[8] = round(dup[8] * rng.uniform(0.3, 1.5), -3)

    candidates = [r for r in rows if r[3] != "Online consumers"]
    plant_duplicates(rng, rows, candidates, DUPLICATE_CUSTOMERS, used, "C", 5, 4,
                     "customer", "customers", mutate)

    # Handpicked: obvious duplicates of well-known customers (no randomness)
    for orig_name, dup_name, variation, since in HANDPICKED_DUPLICATES:
        orig = next(r for r in rows if r[1] == orig_name)
        dup = list(orig)
        dup[0], dup[1], dup[9] = f"C{len(rows) + 1:05d}", dup_name, date(*since)
        rows.append(dup)
        record_issue("Duplicate customer", "customers", dup[0], orig[0],
                     f"'{dup_name}' is the same company as '{orig_name}' ({variation})")
    insert_rows(con, "customers", rows)


def fill_suppliers(con):
    """Brands, private-label factories and service vendors."""
    rng = random.Random(f"{SEED}-suppliers")
    entities = {e: (country, currency) for e, country, currency in
                con.execute("SELECT entity_id, country_code, currency_code FROM entities").fetchall()}
    rows, used = [], set()

    def add(name, stype, category, brand, country, currency, terms, account, entity_id):
        rows.append([name, stype, category, brand, country, currency, terms, account, entity_id])
        used.add(name)

    # Goods: handwritten brands and factories
    for name, brand, country, currency, scope, _ in PUN_GOODS_SUPPLIERS:
        category = ITEM_INFO[resolve_items(scope)[0]][0]
        add(name, "Goods", category, brand, country, currency,
            rng.choice([30, 45, 60]), 4000, None)

    # Goods: small generated brands from the Nordics and Germany
    countries = ["NO", "SE", "DK", "FI", "DE"]
    currency_of = {"NO": "NOK", "SE": "SEK", "DK": "DKK", "FI": "EUR", "DE": "EUR"}
    for _ in range(SMALL_BRAND_SUPPLIERS):
        country = rng.choices(countries, weights=[3, 3, 1, 1, 2])[0]
        loc = LOCALE[country]
        brand = unique_name(rng, used, lambda: f"{rng.choice(loc['nature'])} {rng.choice(SMALL_BRAND_WORDS)}")
        category = rng.choices(list(CATEGORY_MARGIN), weights=[30, 15, 15, 12, 8, 8, 6, 6])[0]
        add(f"{brand} {LEGAL_SUFFIX[country]}", "Goods", category, brand, country,
            currency_of[country], rng.choice([30, 45, 60]), 4000, None)

    # Services: handwritten
    for name, country, currency, category, entity_id in PUN_SERVICE_SUPPLIERS:
        add(name, "Services", category, None, country, currency,
            rng.choice([14, 20, 30, 30]), SERVICE_CATEGORY_ACCOUNT[category], entity_id)

    # Services: generated local vendors per entity
    categories = list(SERVICE_CATEGORY_WEIGHT)
    for entity_id, n in SERVICE_SUPPLIERS_PER_ENTITY.items():
        country, currency = entities[entity_id]
        loc = LOCALE[country]
        for _ in range(n):
            category = rng.choices(categories, weights=list(SERVICE_CATEGORY_WEIGHT.values()))[0]
            name, _ = unique_name(rng, used, lambda: fill_template(
                rng, rng.choice(loc["services"][category]), loc))
            add(name, "Services", category, None, country, currency,
                rng.choice([14, 20, 30, 30]), SERVICE_CATEGORY_ACCOUNT[category], entity_id)

    rng.shuffle(rows)
    rows = [[f"S{i:04d}"] + r for i, r in enumerate(rows, 1)]

    # Row layout: id, name, type, category, brand, country, currency, terms, account, entity
    def mutate(dup, variation):
        if rng.random() < 0.5:
            dup[7] = rng.choice([14, 20, 30, 45])

    plant_duplicates(rng, rows, rows[:], DUPLICATE_SUPPLIERS, used, "S", 4, 5,
                     "supplier", "suppliers", mutate)

    # Story: Roger's shell supplier, added last (no randomness)
    for shell in SHELL_SUPPLIERS:
        rows.append([f"S{len(rows) + 1:04d}"] + list(shell))

    # Bank accounts (own random stream, so the rest is unchanged). A duplicate
    # has the same account as its original; the shell suppliers are paid to
    # Roger's own accounts.
    bank_rng = random.Random(f"{SEED}-supplier-bank")
    fmt = lambda c: IBAN_FORMAT.get(c, c + "dd dddd dddd dddd dddd dd")
    for r in rows:
        r.append("".join(str(bank_rng.randint(0, 9)) if ch == "d" else ch for ch in fmt(r[5])))
    by_id = {r[0]: r for r in rows}
    for issue in PLANTED_ISSUES:
        if issue["issue_type"] == "Duplicate supplier":
            by_id[issue["record_id"]][10] = by_id[issue["related_id"]][10]
    for r in rows:
        if r[1] == "Bakke Rådgivning ENK":
            r[10] = ROGER_SALARY_ACCOUNT
            record_issue("Supplier owned by employee", "suppliers", r[0], "E00634",
                         f"'{r[1]}' is Roger Bakke's own sole proprietorship: same surname, and its bank "
                         f"account {ROGER_SALARY_ACCOUNT} is the account his salary is paid to")
        if r[1] == "Fjellvann Rådgivning AS":
            r[10] = ROGER_SECOND_ACCOUNT
            record_issue("Supplier bank account belongs to employee", "suppliers", r[0], "E00634",
                         f"'{r[1]}' has bank account {ROGER_SECOND_ACCOUNT}, the same account Roger "
                         f"Bakke's second (duplicate) salary payments go to; no name link")
    insert_rows(con, "suppliers", rows)


EMAIL_DOMAIN = {"NO01": "nordvidde.no", "SE01": "nordvidde.se", "DK01": "nordvidde.dk",
                "FI01": "nordvidde.fi", "DE01": "nordvidde.de"}


def fill_users(con):
    """Handwritten employees plus integration accounts. No randomness."""
    rows = []
    for user_id, name, entity_id, department, title, created, deactivated in USERS:
        local = name.lower().translate(ASCII_MAP).replace(" ", ".")
        rows.append([user_id, name, "Person", entity_id, department, title,
                     f"{local}@{EMAIL_DOMAIN[entity_id]}", date(*created),
                     date(*deactivated) if deactivated else None])
    for user_id, description, entity_id, created in SYSTEM_USERS:
        rows.append([user_id, description, "System", entity_id, "IT", "Integration account",
                     None, date(*created), None])
    insert_rows(con, "users", rows)


# Department: (share of generated staff, monthly salary range in NOK at the
# Norwegian 2023 level, job titles)
EMP_DEPARTMENTS = {
    "Warehouse & logistics": (0.48, (32_000, 42_000), ["Warehouse operative", "Picker",
                                                        "Forklift driver", "Shift leader"]),
    "Customer service":      (0.10, (35_000, 45_000), ["Customer service agent", "Order handler"]),
    "Sales":                 (0.16, (45_000, 75_000), ["Sales representative", "Key account manager",
                                                        "Sales coordinator"]),
    "Purchasing":            (0.06, (50_000, 70_000), ["Buyer", "Category manager"]),
    "Marketing":             (0.06, (50_000, 75_000), ["Marketing coordinator", "Content producer",
                                                        "E-commerce specialist"]),
    "Finance":               (0.06, (50_000, 80_000), ["Accountant", "Payroll officer", "Controller"]),
    "IT":                    (0.05, (60_000, 90_000), ["Developer", "IT support", "Data analyst"]),
    "Management":            (0.03, (90_000, 160_000), ["Director", "Head of department"]),
}
USER_DEPARTMENT = {"Logistics": "Warehouse & logistics"}
COUNTRY_PAY_LEVEL = {"NO": 1.0, "SE": 0.95, "DK": 1.15, "FI": 0.9, "DE": 1.0}
EMPLOYEE_TURNOVER = 0.08          # share leaving per year; each leaver is replaced
EMPLOYEE_GROWTH = 0.03            # extra hires per year, share of starting headcount
EMPLOYEE_HORIZON = date(2030, 12, 31)   # generated this far, then cut at END_DATE
IBAN_FORMAT = {"NO": "NOdd dddd dddd ddd", "SE": "SEdd dddd dddd dddd dddd dddd",
               "DK": "DKdd dddd dddd dddd dd", "FI": "FIdd dddd dddd dddd dd",
               "DE": "DEdd dddd dddd dddd dddd dd"}


def pay_raises(d):
    """Number of 1 April pay rises from 2023 up to and including date d."""
    if d < date(2023, 4, 1):
        return 0
    return d.year - 2023 + (1 if d >= date(d.year, 4, 1) else 0)


def fill_employees(con):
    """ERP users plus generated staff per entity. Staff leave at random and
    are replaced; headcount also grows a little each year. Generated up to
    EMPLOYEE_HORIZON and cut at END_DATE, so IDs (in hire order) are stable."""
    rng = random.Random(f"{SEED}-employees")
    entities = {e: (country, currency) for e, country, currency in
                con.execute("SELECT entity_id, country_code, currency_code FROM entities").fetchall()}
    users = con.execute("""
        SELECT user_id, full_name, entity_id, department, job_title, created_date, deactivated_date
        FROM users WHERE user_type = 'Person' ORDER BY user_id""").fetchall()
    depts = list(EMP_DEPARTMENTS)
    used = {u[1] for u in users}
    rows = []   # [name, entity, dept, title, user_id, hire, termination, salary (NOK, 2023 level)]

    def salary(dept, country):
        lo, hi = EMP_DEPARTMENTS[dept][1]
        return rng.uniform(lo, hi) * COUNTRY_PAY_LEVEL[country]

    def leave_date(hired):
        d = max(hired, START_DATE) + timedelta(days=int(rng.expovariate(EMPLOYEE_TURNOVER) * 365.25))
        return d if d <= EMPLOYEE_HORIZON else None

    def hire(entity_id, dept, hired):
        """Add a generated employee, and replacements for as long as they leave."""
        country = entities[entity_id][0]
        while hired and hired <= EMPLOYEE_HORIZON:
            name = unique_name(rng, used, lambda: f"{rng.choice(FIRST_NAMES[country])} "
                                                  f"{rng.choice(LOCALE[country]['surnames'])}")
            left = leave_date(hired)
            rows.append([name, entity_id, dept, rng.choice(EMP_DEPARTMENTS[dept][2]), None,
                         hired, left, salary(dept, country)])
            hired = left + timedelta(days=rng.randint(20, 60)) if left else None

    for user_id, name, entity_id, dept, title, created, deactivated in users:
        dept = USER_DEPARTMENT.get(dept, dept)
        rows.append([name, entity_id, dept, title, user_id, created, deactivated,
                     salary(dept, entities[entity_id][0])])
    weights = [EMP_DEPARTMENTS[d][0] for d in depts]
    for entity_id, n in HEADCOUNT.items():
        for _ in range(n - sum(1 for u in users if u[2] == entity_id)):
            hire(entity_id, rng.choices(depts, weights)[0],
                 random_date(rng, date(2005, 1, 1), START_DATE - timedelta(days=1)))
        for year in range(START_DATE.year, EMPLOYEE_HORIZON.year + 1):
            for _ in range(round(n * EMPLOYEE_GROWTH)):
                hire(entity_id, rng.choices(depts, weights)[0],
                     random_date(rng, date(year, 1, 1), date(year, 12, 31)))

    bank = [IBAN_FORMAT[entities[r[1]][0]] for r in rows]
    bank = ["".join(str(rng.randint(0, 9)) if ch == "d" else ch for ch in fmt) for fmt in bank]
    bank[next(i for i, r in enumerate(rows) if r[4] == "rogerb")] = ROGER_SALARY_ACCOUNT   # story
    out = []
    for r, account in zip(rows, bank):
        name, entity_id, dept, title, user_id, hired, left, nok = r
        if hired > END_DATE:
            continue
        left = left if left and left <= END_DATE else None
        currency = entities[entity_id][1]
        current = nok * (1 + SALARY_RAISE) ** pay_raises(min(left or END_DATE, END_DATE))
        out.append([name, entity_id, dept, title, user_id, hired, left,
                    round(current / APPROX_FX_TO_NOK[currency], -2), currency, account])
    out.sort(key=lambda r: (r[5], r[0]))
    out = [[f"E{i:05d}"] + r for i, r in enumerate(out, 1)]

    # Story: two employees in SE01 have the same bank account (one of them
    # gets the other's salary too, or one is a ghost)
    cand = [r for r in out if r[2] == "SE01" and r[5] is None and r[6] < START_DATE]   # stable set
    a, b = random.Random(f"{SEED}-shared-bank").sample(cand, 2)
    b[10] = a[10]
    record_issue("Employees share a bank account", "employees", b[0], a[0],
                 f"{b[1]} ({b[0]}) and {a[1]} ({a[0]}) at SE01 have the same bank account {a[10]}")
    insert_rows(con, "employees", out)


def fill_products(con):
    """Products from the goods suppliers. Big brands carry more products."""
    rng = random.Random(f"{SEED}-products")
    handwritten = {name: (scope, weight) for name, _, _, _, scope, weight in PUN_GOODS_SUPPLIERS}
    suppliers = []
    for sid, name, brand, category, currency in con.execute("""
            SELECT supplier_id, supplier_name, brand_name, category, currency_code
            FROM suppliers WHERE supplier_type = 'Goods' ORDER BY supplier_id
            """).fetchall():
        scope, weight = handwritten.get(name, ([category], 1))
        suppliers.append((sid, brand, currency, resolve_items(scope), weight))

    # Products always belong to the original supplier, never a planted duplicate
    original_of = {i["record_id"]: i["related_id"] for i in PLANTED_ISSUES
                   if i["table_name"] == "suppliers"}

    rows, used = [], set()
    for i in range(1, N_PRODUCTS + 1):
        sid, brand, currency, items, _ = rng.choices(suppliers, weights=[s[4] for s in suppliers])[0]
        sid = original_of.get(sid, sid)
        item = rng.choice(items)
        category, lo, hi, season = ITEM_INFO[item]
        name = unique_name(rng, used, lambda: (
            f"{brand} {rng.choice(MODEL_NAMES)}{rng.choice(MODEL_VARIANTS)} {item}"))

        list_price = price_point(rng.uniform(lo, hi))
        margin = CATEGORY_MARGIN[category] + rng.uniform(-0.05, 0.05)
        if brand == "Nordvidde":
            margin += PRIVATE_LABEL_EXTRA_MARGIN
        unit_cost = round(list_price * (1 - margin) / APPROX_FX_TO_NOK[currency], 2)

        # Most products existed before the period; some launch during it,
        # and a few are discontinued along the way.
        if rng.random() < 0.8:
            launch = random_date(rng, date(2015, 1, 1), START_DATE - timedelta(days=1))
        else:
            launch = random_date(rng, START_DATE, LAST_NEW_DATE)
        discontinued = None
        if rng.random() < 0.08:
            earliest = max(START_DATE, launch + timedelta(days=180))
            if earliest < DISCONTINUE_UNTIL:
                discontinued = random_date(rng, earliest, DISCONTINUE_UNTIL)

        rows.append([f"P{i:05d}", name, brand, category, item, season, sid, currency,
                     unit_cost, list_price, launch, discontinued])

    insert_rows(con, "products", rows)
