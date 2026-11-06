CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Supplier AS
SELECT
    l.levnr                         AS Supplier_Key,
    l.levnr                         AS SupplierID,
    trim(l.levnavn)                 AS SupplierName,
    l.levtype                       AS SupplierType,
    l.kategori                      AS SupplierCategory,
    l.merke                         AS BrandName,
    l.landkode                      AS CountryCode,
    l.valuta                        AS SupplierCurrencyCode,
    l.betbet                        AS PaymentTermsDays,
    l.std_konto                     AS DefaultAccountID,
    l.firma                         AS CompanyID,
    l.bankkonto                     AS BankAccountNo
FROM
    MakeDataSmart2026.mds.leverandor l;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Supplier IS
'One row per supplier. Join to Fact_GeneralLedger and Fact_Subledger (AP rows) on Supplier_Key.';
