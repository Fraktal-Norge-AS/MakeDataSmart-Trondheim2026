CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Fact_Payroll AS
SELECT
    -- Keys
    p.firma                                           AS Company_Key,
    trim(p.ansattnr)                                  AS Employee_Key,
    p.utbetalt_dato                                   AS PaymentDate_Key,
    CAST(p.periode || '-01' AS DATE)                  AS PayPeriod_Key,

    -- Attributes
    p.utbetalingsnr                                   AS PaymentID,
    p.periode                                         AS PayPeriod,
    p.bankkonto                                       AS BankAccountNo,
    p.bilagsnr                                        AS JournalID,
    p.utbetalt_dato                                   AS ExchangeRateDate,

    -- Measures
    p.valuta                                          AS CompanyCurrencyCode,
    p.brutto                                          AS GrossAmount,
    p.forskuddstrekk                                  AS TaxWithheld,
    p.netto                                           AS NetAmount,
    round(p.brutto * k.kurs, 2)                       AS GrossAmountNOK,
    round(p.netto * k.kurs, 2)                        AS NetAmountNOK
FROM
    MakeDataSmart2026.mds.lonnsutbetaling p
LEFT JOIN
    MakeDataSmart2026.mds.valutakurs k
        ON k.valuta = p.valuta
       AND k.kursdato = p.utbetalt_dato;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Fact_Payroll IS
'Salary payments, one row per payment. Join to dimensions on Company_Key and Employee_Key, and to Dim_Date on PaymentDate_Key or PayPeriod_Key (first day of the pay month).';
