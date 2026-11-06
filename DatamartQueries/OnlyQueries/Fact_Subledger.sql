CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Fact_Subledger AS
WITH ar_invoice AS (
    -- Customer invoices and credit notes, with the shared invoice information
    SELECT
        f.fakturanr                                   AS invoice_id,
        f.firma                                       AS company_id,
        trim(f.kundenr)                               AS customer_id,         -- fix: trailing spaces (DK01, Mar-Apr 2025)
        f.kons_firma                                  AS ic_company_id,
        f.fakturatype                                 AS invoice_type,
        f.fakturadato                                 AS invoice_date,
        f.forfall                                     AS due_date,
        COALESCE(o1.ordrenr, o2.ordrenr)              AS order_id,            -- fix: SYS_SPECORD invoices hold the internal order key
        f.valuta                                      AS currency_code,
        f.belop                                       AS amount,
        f.bilagsnr                                    AS journal_id
    FROM
        MakeDataSmart2026.mds.kundefaktura f
    LEFT JOIN
        MakeDataSmart2026.mds.ordre o1
            ON o1.ordrenr = f.ordre_id
    LEFT JOIN
        MakeDataSmart2026.mds.ordre o2
            ON o2.ordre_id = f.ordre_id
),
transactions AS (
    -- AR invoices
    SELECT
        'AR'                                          AS subledger_type,
        'Invoice'                                     AS transaction_category,
        i.invoice_type                                AS transaction_type,
        i.company_id                                  AS company_id,
        i.customer_id                                 AS customer_id,
        NULL                                          AS supplier_id,
        i.ic_company_id                               AS ic_company_id,
        i.invoice_date                                AS transaction_date,
        i.invoice_date                                AS invoice_date,
        i.due_date                                    AS due_date,
        i.invoice_id                                  AS invoice_id,
        i.invoice_id                                  AS document_id,
        NULL                                          AS supplier_invoice_no,
        i.order_id                                    AS order_id,
        NULL                                          AS payment_reference,
        i.journal_id                                  AS journal_id,
        i.currency_code                               AS currency_code,
        i.amount                                      AS amount
    FROM
        ar_invoice i

    UNION ALL

    -- AR payments and write-offs
    SELECT
        'AR'                                          AS subledger_type,
        'Payment'                                     AS transaction_category,
        p.betalingstype                               AS transaction_type,
        p.firma                                       AS company_id,
        i.customer_id                                 AS customer_id,
        NULL                                          AS supplier_id,
        i.ic_company_id                               AS ic_company_id,
        p.betalt_dato                                 AS transaction_date,
        i.invoice_date                                AS invoice_date,
        i.due_date                                    AS due_date,
        p.fakturanr                                   AS invoice_id,
        p.innbetalingsnr                              AS document_id,
        NULL                                          AS supplier_invoice_no,
        i.order_id                                    AS order_id,
        p.referanse                                   AS payment_reference,
        p.bilagsnr                                    AS journal_id,
        p.valuta                                      AS currency_code,
        -p.belop                                      AS amount
    FROM
        MakeDataSmart2026.mds.kundeinnbetaling p
    LEFT JOIN
        ar_invoice i
            ON i.invoice_id = p.fakturanr

    UNION ALL

    -- AP invoices
    SELECT
        'AP'                                          AS subledger_type,
        'Invoice'                                     AS transaction_category,
        v.fakturatype                                 AS transaction_type,
        v.firma                                       AS company_id,
        NULL                                          AS customer_id,
        trim(v.levnr)                                 AS supplier_id,
        v.kons_firma                                  AS ic_company_id,
        v.fakturadato                                 AS transaction_date,
        v.fakturadato                                 AS invoice_date,
        v.forfall                                     AS due_date,
        v.fakturanr                                   AS invoice_id,
        v.fakturanr                                   AS document_id,
        v.lev_fakturanr                               AS supplier_invoice_no,
        NULL                                          AS order_id,
        NULL                                          AS payment_reference,
        v.bilagsnr                                    AS journal_id,
        v.valuta                                      AS currency_code,
        v.belop                                       AS amount
    FROM
        MakeDataSmart2026.mds.levfaktura v

    UNION ALL

    -- AP payments
    SELECT
        'AP'                                          AS subledger_type,
        'Payment'                                     AS transaction_category,
        'Payment'                                     AS transaction_type,
        u.firma                                       AS company_id,
        NULL                                          AS customer_id,
        trim(v.levnr)                                 AS supplier_id,
        v.kons_firma                                  AS ic_company_id,
        u.betalt_dato                                 AS transaction_date,
        v.fakturadato                                 AS invoice_date,
        v.forfall                                     AS due_date,
        u.fakturanr                                   AS invoice_id,
        u.utbetalingsnr                               AS document_id,
        v.lev_fakturanr                               AS supplier_invoice_no,
        NULL                                          AS order_id,
        NULL                                          AS payment_reference,
        u.bilagsnr                                    AS journal_id,
        u.valuta                                      AS currency_code,
        -u.belop                                      AS amount
    FROM
        MakeDataSmart2026.mds.levutbetaling u
    LEFT JOIN
        MakeDataSmart2026.mds.levfaktura v
            ON v.fakturanr = u.fakturanr
)
SELECT
    -- Keys
    t.company_id                                      AS Company_Key,
    t.customer_id                                     AS Customer_Key,
    t.supplier_id                                     AS Supplier_Key,
    t.ic_company_id                                   AS InterCompany_Key,
    t.transaction_date                                AS TransactionDate_Key,
    t.invoice_date                                    AS InvoiceDate_Key,
    t.due_date                                        AS DueDate_Key,

    -- Attributes
    t.subledger_type                                  AS SubledgerType,
    t.transaction_category                            AS TransactionCategory,
    t.transaction_type                                AS TransactionType,
    t.invoice_id                                      AS InvoiceID,
    t.document_id                                     AS DocumentID,
    t.supplier_invoice_no                             AS SupplierInvoiceNo,
    t.order_id                                        AS OrderID,
    t.payment_reference                               AS PaymentReference,
    t.journal_id                                      AS JournalID,
    greatest(t.transaction_date, DATE '2023-01-01')   AS ExchangeRateDate,

    -- Measures (positive = increases the open balance, for both AR and AP)
    t.currency_code                                   AS DocumentCurrencyCode,
    t.amount                                          AS AmountDocumentCurrency,
    round(t.amount * k.kurs, 2)                       AS AmountNOK
FROM
    transactions t
LEFT JOIN
    MakeDataSmart2026.mds.valutakurs k
        ON k.valuta = t.currency_code
       AND k.kursdato = greatest(t.transaction_date, DATE '2023-01-01');
