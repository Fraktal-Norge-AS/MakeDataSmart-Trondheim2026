"""
Final step of the build: rename every table and column to Norwegian ERP-style
names, as in an older Norwegian accounting system. The code works with the
English names; only the finished database gets these.

Deliberate traps for the demo AI (recorded in the answer key):
  - ordre.ordre_id is an internal integer key (used by ordrelinje), while
    kundefaktura.ordre_id holds the order NUMBER, which is ordre.ordrenr.
  - belop is the entity's currency in hovedbok_linjer, but the document
    currency in the subledgers; belop_val is the transaction currency.
  - bilagsnr (voucher) appears everywhere; fakturanr is the subledger number.
"""

# table: (new table name, {old column: new column})
NAMES = {
    "entities": ("firma", {
        "entity_id": "firma", "entity_name": "firmanavn", "country_code": "landkode",
        "country": "land", "city": "sted", "currency_code": "valuta", "is_hq": "hovedkontor"}),
    "currencies": ("valuta", {"currency_code": "valuta", "currency_name": "valutanavn"}),
    "chart_of_accounts": ("kontoplan", {
        "account_id": "kontonr", "account_name": "kontonavn", "account_class": "kontoklasse",
        "account_group": "kontogruppe", "statement": "rapporttype"}),
    "dim_date": ("kalender", {
        "date": "dato", "year": "aar", "quarter": "kvartal", "month": "mnd",
        "month_name": "mnd_navn", "year_month": "periode", "iso_week": "uke",
        "day_of_week": "ukedag_nr", "day_name": "ukedag", "is_weekend": "helg"}),
    "fx_rates": ("valutakurs", {
        "rate_date": "kursdato", "currency_code": "valuta", "rate_to_nok": "kurs",
        "rate_source_date": "notert_dato"}),
    "customers": ("kunde", {
        "customer_id": "kundenr", "customer_name": "kundenavn", "entity_id": "firma",
        "segment": "kundegruppe", "country_code": "landkode", "city": "sted",
        "currency_code": "valuta", "payment_terms_days": "betbet", "credit_limit": "kredittgrense",
        "customer_since": "kunde_fra"}),
    "suppliers": ("leverandor", {
        "supplier_id": "levnr", "supplier_name": "levnavn", "supplier_type": "levtype",
        "category": "kategori", "brand_name": "merke", "country_code": "landkode",
        "currency_code": "valuta", "payment_terms_days": "betbet", "default_account_id": "std_konto",
        "entity_id": "firma", "bank_account": "bankkonto"}),
    "products": ("vare", {
        "product_id": "varenr", "product_name": "varenavn", "brand_name": "merke",
        "category": "varegruppe", "product_type": "varetype", "season": "sesong",
        "supplier_id": "levnr", "cost_currency": "innk_valuta", "unit_cost": "innpris",
        "list_price_nok": "listepris", "launch_date": "lansert", "discontinued_date": "utgaatt"}),
    "users": ("bruker", {
        "user_id": "brukerid", "full_name": "navn", "user_type": "brukertype", "entity_id": "firma",
        "department": "avdeling", "job_title": "stilling", "email": "epost",
        "created_date": "opprettet", "deactivated_date": "deaktivert"}),
    "employees": ("ansatt", {
        "employee_id": "ansattnr", "full_name": "navn", "entity_id": "firma",
        "department": "avdeling", "job_title": "stilling", "user_id": "brukerid",
        "hire_date": "ansatt_dato", "termination_date": "slutt_dato",
        "monthly_salary": "mnd_lonn", "currency_code": "valuta", "bank_account": "bankkonto"}),
    "report_definitions": ("rapport", {
        "report_id": "rapport", "report_name": "rapportnavn", "description": "beskrivelse"}),
    "report_lines": ("rapportlinje", {
        "report_id": "rapport", "line_id": "linje", "line_name": "linjenavn",
        "sort_order": "sortering", "line_type": "linjetype", "sign": "fortegn"}),
    "report_line_mapping": ("rapportoppsett", {
        "mapping_id": "id", "report_id": "rapport", "line_id": "linje",
        "account_from": "fra_konto", "account_to": "til_konto", "entity_id": "firma",
        "product_category": "varegruppe"}),
    "report_line_totals": ("rapportsum", {
        "report_id": "rapport", "total_line_id": "sumlinje", "component_line_id": "linje"}),
    "ar_invoices": ("kundefaktura", {
        "invoice_id": "fakturanr", "entity_id": "firma", "customer_id": "kundenr",
        "ic_entity_id": "kons_firma", "invoice_type": "fakturatype",
        "credited_invoice_id": "kreditert_fakturanr", "invoice_date": "fakturadato",
        "due_date": "forfall", "currency_code": "valuta", "amount": "belop", "vat_amount": "mva",
        "journal_id": "bilagsnr", "order_id": "ordre_id", "comment": "kommentar"}),
    "ar_payments": ("kundeinnbetaling", {
        "payment_id": "innbetalingsnr", "entity_id": "firma", "invoice_id": "fakturanr",
        "payment_type": "betalingstype", "reference": "referanse", "payment_date": "betalt_dato",
        "currency_code": "valuta",
        "amount": "belop", "journal_id": "bilagsnr"}),
    "ap_invoices": ("levfaktura", {
        "invoice_id": "fakturanr", "supplier_invoice_no": "lev_fakturanr", "entity_id": "firma",
        "supplier_id": "levnr", "ic_entity_id": "kons_firma", "invoice_type": "fakturatype",
        "invoice_date": "fakturadato", "due_date": "forfall", "currency_code": "valuta",
        "amount": "belop", "vat_amount": "mva", "journal_id": "bilagsnr"}),
    "ap_payments": ("levutbetaling", {
        "payment_id": "utbetalingsnr", "entity_id": "firma", "invoice_id": "fakturanr",
        "payment_date": "betalt_dato", "currency_code": "valuta", "amount": "belop",
        "journal_id": "bilagsnr"}),
    "gl_journals": ("hovedbok_bilag", {
        "journal_id": "bilagsnr", "entity_id": "firma", "posting_date": "bilagsdato",
        "source": "kilde", "document_no": "dokumentnr", "description": "tekst",
        "user_id": "registrert_av", "approved_by": "godkjent_av", "created_at": "registrert_tid"}),
    "gl_lines": ("hovedbok_linje", {
        "journal_id": "bilagsnr", "line_no": "linjenr", "entity_id": "firma",
        "posting_date": "bilagsdato", "account_id": "kontonr", "currency_code": "valuta",
        "amount_currency": "belop_val", "amount": "belop", "customer_id": "kundenr",
        "supplier_id": "levnr", "product_id": "varenr", "ic_entity_id": "kons_firma",
        "quantity": "antall", "line_text": "linjetekst"}),
    "payroll_payments": ("lonnsutbetaling", {
        "payment_id": "utbetalingsnr", "employee_id": "ansattnr", "entity_id": "firma",
        "pay_period": "periode", "payment_date": "utbetalt_dato", "currency_code": "valuta",
        "gross_amount": "brutto", "tax_withheld": "forskuddstrekk", "net_amount": "netto",
        "bank_account": "bankkonto", "journal_id": "bilagsnr"}),
    "sales_orders": ("ordre", {
        "order_key": "ordre_id", "order_id": "ordrenr", "entity_id": "firma",
        "customer_id": "kundenr", "order_type": "ordretype", "order_date": "ordredato",
        "requested_delivery_date": "onsket_lev_dato", "status": "status",
        "currency_code": "valuta", "order_amount": "ordrebelop"}),
    "sales_order_lines": ("ordrelinje", {
        "order_key": "ordre_id", "line_no": "linjenr", "product_id": "varenr", "quantity": "antall",
        "unit_price": "pris", "discount_pct": "rabatt", "line_amount": "belop",
        "quantity_invoiced": "antall_fakt", "quantity_cancelled": "antall_kans"}),
}


def apply_norwegian_names(con):
    """Rename all tables and columns in place (primary keys follow along)."""
    for table, (new_table, columns) in NAMES.items():
        existing = {c for (c,) in con.execute(
            f"SELECT column_name FROM duckdb_columns() WHERE table_name = '{table}'").fetchall()}
        missing = existing - set(columns)
        if missing:
            raise ValueError(f"{table}: no Norwegian name for {sorted(missing)}")
        for old, new in columns.items():
            if old != new:
                con.execute(f'ALTER TABLE {table} RENAME COLUMN "{old}" TO "{new}"')
        con.execute(f"ALTER TABLE {table} RENAME TO {new_table}")


def translate_issue(issue):
    """The answer key refers to the Norwegian table names; English column
    names in descriptions are replaced by the Norwegian ones."""
    issue = dict(issue)
    table, columns = NAMES.get(issue["table_name"], (issue["table_name"], {}))
    issue["table_name"] = table
    text = issue["description"]
    for _, cols in NAMES.values():
        for old, new in cols.items():
            if "_" in old and old in text:          # only real column names like credited_invoice_id
                text = text.replace(old, new)
    for old, (new, _) in NAMES.items():
        if "_" in old and old in text:
            text = text.replace(old, new)
    issue["description"] = text
    return issue


# Schema traps for the answer key (not data issues, but easy mistakes)
SCHEMA_TRAPS = [
    dict(issue_type="Schema trap", table_name="kundefaktura", record_id=None, related_id="ordre",
         description="kundefaktura.ordre_id normally holds the order NUMBER (SO-/WS-...), which is "
                     "ordre.ordrenr; ordre.ordre_id is an internal key (digits) used by ordrelinje.ordre_id. "
                     "But invoices posted by SYS_SPECORD (buggy special-order integration) hold the "
                     "internal key instead. So kundefaktura.ordre_id = ordre.ordre_id matches only the "
                     "SYS_SPECORD invoices (~6%), and = ordre.ordrenr misses exactly those; a correct "
                     "join needs both (join on ordrenr, then on ordre_id for the rest)"),
    dict(issue_type="Schema trap", table_name="hovedbok_linje", record_id=None, related_id=None,
         description="hovedbok_linje.belop is in the entity's currency (firma.valuta) and belop_val in "
                     "the transaction currency (valuta); in kundefaktura/levfaktura/innbetalinger belop "
                     "is in the document currency. Summing belop across firms mixes NOK, SEK, DKK and EUR"),
    dict(issue_type="Schema trap", table_name="ansatt", record_id=None, related_id=None,
         description="ansatt.bankkonto is a bank account number, not an account in kontoplan "
                     "(hovedbok_linje.kontonr)"),
]
