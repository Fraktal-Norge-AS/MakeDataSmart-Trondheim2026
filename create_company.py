"""
Schema for the Nordvidde Group dataset: one create_<table>(con) per table.

Only table definitions live here. The data is inserted by fill_company_data.py.
"""


def create_entities(con):
    """Legal entities in the group. Each books in its own functional currency."""
    con.execute("""
        CREATE TABLE entities (
            entity_id      VARCHAR PRIMARY KEY,
            entity_name    VARCHAR,
            country_code   VARCHAR,
            country        VARCHAR,
            city           VARCHAR,
            currency_code  VARCHAR,   -- functional currency
            is_hq          BOOLEAN
        )
    """)


def create_currencies(con):
    """Currencies used. FX rates are supplied separately."""
    con.execute("""
        CREATE TABLE currencies (
            currency_code  VARCHAR PRIMARY KEY,
            currency_name  VARCHAR
        )
    """)


def create_chart_of_accounts(con):
    """Simplified chart of accounts using Norwegian standard (NS 4102) numbering."""
    con.execute("""
        CREATE TABLE chart_of_accounts (
            account_id     INTEGER PRIMARY KEY,
            account_name   VARCHAR,
            account_class  VARCHAR,   -- Asset, Liability, Equity, Revenue, Expense
            account_group  VARCHAR,   -- grouping for reporting (P&L / balance sheet lines)
            statement      VARCHAR    -- 'BS' (balance sheet) or 'PL' (profit and loss)
        )
    """)


def create_dim_date(con):
    """Calendar table covering the full period."""
    con.execute("""
        CREATE TABLE dim_date (
            date           DATE PRIMARY KEY,
            year           INTEGER,
            quarter        INTEGER,
            month          INTEGER,
            month_name     VARCHAR,
            year_month     VARCHAR,
            iso_week       INTEGER,
            day_of_week    INTEGER,   -- 1 = Monday
            day_name       VARCHAR,
            is_weekend     BOOLEAN
        )
    """)


def create_fx_rates(con):
    """Daily exchange rates to NOK for every date in the period, NOK included."""
    con.execute("""
        CREATE TABLE fx_rates (
            rate_date         DATE,      -- -> dim_date
            currency_code     VARCHAR,   -- -> currencies
            rate_to_nok       DECIMAL(18, 6),  -- NOK per 1 unit of currency_code
            rate_source_date  DATE,      -- business day the rate was published
                                         -- (weekends and holidays use the previous one)
            PRIMARY KEY (rate_date, currency_code)
        )
    """)


def create_customers(con):
    """Retail customers. Each belongs to the group entity that sells to it."""
    con.execute("""
        CREATE TABLE customers (
            customer_id        VARCHAR PRIMARY KEY,
            customer_name      VARCHAR,
            entity_id          VARCHAR,   -- selling entity -> entities
            segment            VARCHAR,   -- Key account, Chain store, Independent, Webshop, Online consumers
            country_code       VARCHAR,
            city               VARCHAR,
            currency_code      VARCHAR,   -- invoicing currency -> currencies
            payment_terms_days INTEGER,
            credit_limit       DECIMAL(18, 2),  -- in invoicing currency
            customer_since     DATE
        )
    """)


def create_suppliers(con):
    """Goods suppliers (brands and contract factories) and service vendors."""
    con.execute("""
        CREATE TABLE suppliers (
            supplier_id        VARCHAR PRIMARY KEY,
            supplier_name      VARCHAR,
            supplier_type      VARCHAR,   -- Goods or Services
            category           VARCHAR,   -- product category or service category
            brand_name         VARCHAR,   -- goods only; 'Nordvidde' = our private label
            country_code       VARCHAR,
            currency_code      VARCHAR,   -- invoicing currency -> currencies
            payment_terms_days INTEGER,
            default_account_id INTEGER,   -- -> chart_of_accounts
            entity_id          VARCHAR,   -- -> entities; NULL = used group-wide
            bank_account       VARCHAR    -- account payments are made to
        )
    """)


def create_users(con):
    """ERP users: employees and integration accounts that post to the ledger."""
    con.execute("""
        CREATE TABLE users (
            user_id           VARCHAR PRIMARY KEY,   -- login name
            full_name         VARCHAR,   -- person's name, or description for system users
            user_type         VARCHAR,   -- Person or System
            entity_id         VARCHAR,   -- home entity -> entities; NULL = group-wide
            department        VARCHAR,
            job_title         VARCHAR,
            email             VARCHAR,
            created_date      DATE,
            deactivated_date  DATE       -- NULL = still active
        )
    """)


def create_ar_invoices(con):
    """Customer ledger: sales invoices and credit notes (credit notes are negative)."""
    con.execute("""
        CREATE TABLE ar_invoices (
            invoice_id          VARCHAR PRIMARY KEY,
            entity_id           VARCHAR,   -- selling entity -> entities
            customer_id         VARCHAR,   -- -> customers; NULL for intercompany
            ic_entity_id        VARCHAR,   -- buying group entity -> entities; NULL = external
            invoice_type        VARCHAR,   -- Invoice or Credit note
            credited_invoice_id VARCHAR,   -- credit notes: -> ar_invoices
            invoice_date        DATE,
            due_date            DATE,
            currency_code       VARCHAR,   -- -> currencies
            amount              DECIMAL(18, 2),  -- incl. VAT, in currency_code
            vat_amount          DECIMAL(18, 2),  -- in currency_code
            journal_id          BIGINT,    -- -> gl_journals
            order_id            VARCHAR,   -- order number -> sales_orders.order_id (not order_key);
                                           -- NULL for credit notes and intercompany. (Story: the
                                           -- SYS_SPECORD integration writes order_key here instead.)
            comment             VARCHAR    -- free text, e.g. the reason for a credit note
        )
    """)


def create_sales_orders(con):
    """Customer orders (B2B and webshop). Invoices refer to their order."""
    con.execute("""
        CREATE TABLE sales_orders (
            order_key                VARCHAR PRIMARY KEY,  -- internal key (digits), used by the order lines
            order_id                 VARCHAR,   -- order number (SO-/WS-), used by the invoices
            entity_id                VARCHAR,   -- -> entities
            customer_id              VARCHAR,   -- -> customers
            order_type               VARCHAR,   -- B2B or Webshop
            order_date               DATE,
            requested_delivery_date  DATE,
            status                   VARCHAR,   -- Open, Partly invoiced, Invoiced, Invoiced - rest
                                                -- cancelled, Cancelled, Blocked - credit limit,
                                                -- Blocked - credit hold
            currency_code            VARCHAR,   -- -> currencies
            order_amount             DECIMAL(18, 2)  -- excl. VAT, as ordered
        )
    """)


def create_sales_order_lines(con):
    """Order lines: what was ordered, invoiced and cancelled."""
    con.execute("""
        CREATE TABLE sales_order_lines (
            order_key           VARCHAR,   -- -> sales_orders.order_key (not the order number)
            line_no             INTEGER,
            product_id          VARCHAR,   -- -> products
            quantity            INTEGER,   -- ordered
            unit_price          DECIMAL(18, 2),  -- price list, order currency
            discount_pct        DECIMAL(5, 1),
            line_amount         DECIMAL(18, 2),  -- quantity x net price
            quantity_invoiced   INTEGER,
            quantity_cancelled  INTEGER,
            PRIMARY KEY (order_key, line_no)
        )
    """)


def create_ar_payments(con):
    """Customer payments and write-offs, each applied to one invoice
    (partial payments allowed)."""
    con.execute("""
        CREATE TABLE ar_payments (
            payment_id     VARCHAR PRIMARY KEY,
            entity_id      VARCHAR,   -- -> entities
            invoice_id     VARCHAR,   -- -> ar_invoices
            payment_type   VARCHAR,   -- Bank or Write-off
            reference      VARCHAR,   -- what the payer wrote (free text)
            payment_date   DATE,
            currency_code  VARCHAR,   -- -> currencies
            amount         DECIMAL(18, 2),  -- in currency_code
            journal_id     BIGINT     -- -> gl_journals
        )
    """)


def create_ap_invoices(con):
    """Supplier ledger: purchase invoices and credit notes (credit notes are negative)."""
    con.execute("""
        CREATE TABLE ap_invoices (
            invoice_id          VARCHAR PRIMARY KEY,   -- our internal number
            supplier_invoice_no VARCHAR,   -- the number on the supplier's invoice
            entity_id           VARCHAR,   -- buying entity -> entities
            supplier_id         VARCHAR,   -- -> suppliers; NULL for intercompany
            ic_entity_id        VARCHAR,   -- selling group entity -> entities; NULL = external
            invoice_type        VARCHAR,   -- Invoice or Credit note
            invoice_date        DATE,
            due_date            DATE,
            currency_code       VARCHAR,   -- -> currencies
            amount              DECIMAL(18, 2),  -- incl. VAT, in currency_code
            vat_amount          DECIMAL(18, 2),  -- in currency_code
            journal_id          BIGINT     -- -> gl_journals
        )
    """)


def create_ap_payments(con):
    """Payments to suppliers, each applied to one invoice."""
    con.execute("""
        CREATE TABLE ap_payments (
            payment_id     VARCHAR PRIMARY KEY,
            entity_id      VARCHAR,   -- -> entities
            invoice_id     VARCHAR,   -- -> ap_invoices
            payment_date   DATE,
            currency_code  VARCHAR,   -- -> currencies
            amount         DECIMAL(18, 2),  -- in currency_code
            journal_id     BIGINT     -- -> gl_journals
        )
    """)


def create_gl_journals(con):
    """General ledger vouchers (one per business event)."""
    con.execute("""
        CREATE TABLE gl_journals (
            journal_id     BIGINT PRIMARY KEY,
            entity_id      VARCHAR,   -- -> entities
            posting_date   DATE,      -- accounting date -> dim_date
            source         VARCHAR,   -- AR, AP, BANK, INVENTORY, PAYROLL, IC, CLOSE or MANUAL
            document_no    VARCHAR,   -- subledger document (invoice or payment id); NULL for manual
            description    VARCHAR,
            user_id        VARCHAR,   -- who posted it -> users
            approved_by    VARCHAR,   -- who approved it -> users; NULL = automatic posting
            created_at     TIMESTAMP  -- when it was entered (can differ from posting_date)
        )
    """)


def create_gl_lines(con):
    """General ledger lines. Debit is positive, credit negative.
    amount (entity currency) sums to zero per journal."""
    con.execute("""
        CREATE TABLE gl_lines (
            journal_id       BIGINT,    -- -> gl_journals
            line_no          INTEGER,
            entity_id        VARCHAR,   -- -> entities (copied from the journal)
            posting_date     DATE,      -- copied from the journal
            account_id       INTEGER,   -- -> chart_of_accounts
            currency_code    VARCHAR,   -- transaction currency -> currencies
            amount_currency  DECIMAL(18, 2),  -- in currency_code
            amount           DECIMAL(18, 2),  -- in the entity's functional currency
            customer_id      VARCHAR,   -- -> customers
            supplier_id      VARCHAR,   -- -> suppliers
            product_id       VARCHAR,   -- -> products; set on revenue, COGS and inventory lines
            ic_entity_id     VARCHAR,   -- intercompany counterparty -> entities
            quantity         INTEGER,
            line_text        VARCHAR,   -- free text from the source system, if any
            PRIMARY KEY (journal_id, line_no)
        )
    """)


def create_employees(con):
    """Employees of the group. ERP users are a subset (user_id set)."""
    con.execute("""
        CREATE TABLE employees (
            employee_id       VARCHAR PRIMARY KEY,
            full_name         VARCHAR,
            entity_id         VARCHAR,   -- employing entity -> entities
            department        VARCHAR,
            job_title         VARCHAR,
            user_id           VARCHAR,   -- ERP login -> users; NULL = no login
            hire_date         DATE,
            termination_date  DATE,      -- NULL = still employed
            monthly_salary    DECIMAL(18, 2),  -- latest (or last) monthly salary
            currency_code     VARCHAR,   -- -> currencies
            bank_account      VARCHAR    -- account salaries are paid to
        )
    """)


def create_payroll_payments(con):
    """Payroll subledger: one salary payment per employee per month."""
    con.execute("""
        CREATE TABLE payroll_payments (
            payment_id      VARCHAR PRIMARY KEY,
            employee_id     VARCHAR,   -- -> employees
            entity_id       VARCHAR,   -- -> entities
            pay_period      VARCHAR,   -- YYYY-MM
            payment_date    DATE,
            currency_code   VARCHAR,   -- -> currencies
            gross_amount    DECIMAL(18, 2),  -- salary incl. bonus
            tax_withheld    DECIMAL(18, 2),
            net_amount      DECIMAL(18, 2),  -- paid to bank_account
            bank_account    VARCHAR,
            journal_id      BIGINT     -- payroll journal -> gl_journals
        )
    """)


def create_report_definitions(con):
    """Financial reports (P&L, balance sheet, management P&L)."""
    con.execute("""
        CREATE TABLE report_definitions (
            report_id      VARCHAR PRIMARY KEY,
            report_name    VARCHAR,
            description    VARCHAR
        )
    """)


def create_report_lines(con):
    """Lines of each report, in display order."""
    con.execute("""
        CREATE TABLE report_lines (
            report_id      VARCHAR,   -- -> report_definitions
            line_id        VARCHAR,
            line_name      VARCHAR,
            sort_order     INTEGER,
            line_type      VARCHAR,   -- header (no value), mapped (from accounts) or total
            sign           INTEGER,   -- mapped lines: report value = sign * sum of ledger amounts
                                      -- (debit positive). NULL for header and total lines.
            PRIMARY KEY (report_id, line_id)
        )
    """)


def create_report_line_mapping(con):
    """Which accounts feed each mapped line. Account ranges are inclusive.
    Optional filters narrow a range to one entity or one product category;
    NULL means no filter. Several rows for one line are added together."""
    con.execute("""
        CREATE TABLE report_line_mapping (
            mapping_id        INTEGER PRIMARY KEY,
            report_id         VARCHAR,   -- -> report_lines
            line_id           VARCHAR,   -- -> report_lines
            account_from      INTEGER,   -- -> chart_of_accounts
            account_to        INTEGER,   -- -> chart_of_accounts
            entity_id         VARCHAR,   -- -> entities; NULL = all entities
            product_category  VARCHAR    -- -> products.category; NULL = all (incl. lines without product)
        )
    """)


def create_report_line_totals(con):
    """Components of each total line. A total is the sum of its components'
    report values; components can be totals themselves."""
    con.execute("""
        CREATE TABLE report_line_totals (
            report_id          VARCHAR,   -- -> report_lines
            total_line_id      VARCHAR,   -- -> report_lines
            component_line_id  VARCHAR,   -- -> report_lines
            PRIMARY KEY (report_id, total_line_id, component_line_id)
        )
    """)


def create_products(con):
    """Products for resale. Each is bought from one supplier."""
    con.execute("""
        CREATE TABLE products (
            product_id         VARCHAR PRIMARY KEY,
            product_name       VARCHAR,
            brand_name         VARCHAR,
            category           VARCHAR,
            product_type       VARCHAR,
            season             VARCHAR,   -- Winter, Summer or All year
            supplier_id        VARCHAR,   -- -> suppliers
            cost_currency      VARCHAR,   -- -> currencies
            unit_cost          DECIMAL(18, 2),  -- purchase price in cost_currency
            list_price_nok     DECIMAL(18, 2),  -- wholesale list price, group price list
            launch_date        DATE,
            discontinued_date  DATE       -- NULL = still sold
        )
    """)
