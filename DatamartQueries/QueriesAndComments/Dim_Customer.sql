CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Customer AS

SELECT
    k.kundenr                       AS Customer_Key,
    k.kundenr                       AS CustomerID,
    TRIM(k.kundenavn)               AS CustomerName,
    k.firma                         AS CompanyID,
    k.kundegruppe                   AS CustomerSegment,
    k.landkode                      AS CountryCode,
    k.sted                          AS City,
    k.valuta                        AS CustomerCurrencyCode,
    k.betbet                        AS PaymentTermsDays,
    k.kredittgrense                 AS CreditLimit,
    k.kunde_fra                     AS CustomerSince
FROM
    MakeDataSmart2026.mds.kunde k;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Customer IS
'One row per customer. Join to Fact_GeneralLedger, Fact_SalesOrders and Fact_Subledger (AR rows) on Customer_Key.';
