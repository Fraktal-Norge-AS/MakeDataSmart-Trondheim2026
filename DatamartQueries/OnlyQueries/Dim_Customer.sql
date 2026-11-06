CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Dim_Customer AS

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
    MakeDataSmart2026.mds.kunde k
