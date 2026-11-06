CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Fact_GeneralLedger AS
SELECT
    -- Keys
    l.firma                                           AS Company_Key,
    l.bilagsdato                                      AS Date_Key,
    l.kontonr                                         AS Account_Key,
    trim(l.kundenr)                                   AS Customer_Key,
    trim(l.levnr)                                     AS Supplier_Key,
     CASE
        WHEN l.varenr IS NOT NULL THEN trim(l.varenr)
        WHEN l.kontonr IN (1460, 3000, 3100, 3200, 3400, 4000, 4300) THEN '-1'   -- product accounts: product missing
    END                                               AS Product_Key,
    l.kons_firma                                      AS InterCompany_Key,
    b.registrert_av                                   AS RegisteredByUser_Key,
    b.godkjent_av                                     AS ApprovedByUser_Key,

    -- Journal (voucher) attributes
    l.bilagsdato                                      as ExchangeRateDate,
    l.bilagsnr                                        AS JournalID,
    l.linjenr                                         AS LineNo,
    b.kilde                                           AS JournalSource,
    b.dokumentnr                                      AS DocumentNo,
    b.tekst                                           AS JournalText,
    l.linjetekst                                      AS LineText,
    b.registrert_tid::DATE                            AS RegisteredDate,
    b.registrert_tid::TIME                            AS RegisteredTime,

    -- Measures
    l.antall                                          AS Quantity,
    l.valuta                                          AS TransactionCurrencyCode,
    l.belop_val                                       AS AmountTransactionCurrency,
    f.valuta                                          AS CompanyCurrencyCode,
    l.belop                                           AS AmountCompanyCurrency,
    round(l.belop * k.kurs, 2)                        AS AmountNOK
FROM
    MakeDataSmart2026.mds.hovedbok_linje l
JOIN
    MakeDataSmart2026.mds.hovedbok_bilag b
        ON b.bilagsnr = l.bilagsnr
JOIN
    MakeDataSmart2026.mds.firma f
        ON f.firma = l.firma
LEFT JOIN
    MakeDataSmart2026.mds.valutakurs k
        ON k.valuta = f.valuta
       AND k.kursdato = l.bilagsdato;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Fact_GeneralLedger IS
'General ledger, one row per journal line. Join to dimensions on Company_Key, Date_Key, Account_Key, Customer_Key, Supplier_Key, Product_Key, InterCompany_Key (Dim_Company) and RegisteredByUser_Key / ApprovedByUser_Key (Dim_User). Revenue and other credits are negative. Use AmountNOK to sum across companies. For report lines (P&L, balance sheet, EBITDA) go through the bridges: Fact_GeneralLedger -> Bridge_MultidimensionalBridge -> Bridge_ReportLineHierarchy -> Dim_ReportLines.';
