CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Product AS
SELECT
    v.varenr                        AS Product_Key,
    v.varenr                        AS ProductID,
    trim(v.varenavn)                AS ProductName,
    v.merke                         AS BrandName,
    v.varegruppe                    AS ProductCategory,
    v.varetype                      AS ProductType,
    v.sesong                        AS Season,
   -- v.levnr                         AS SupplierID,
    v.innk_valuta                   AS PurchaseCurrencyCode,
    v.innpris                       AS UnitCost,
    v.listepris                     AS ListPriceNOK,
    v.lansert                       AS LaunchDate,
    v.utgaatt                       AS DiscontinuedDate,
    v.utgaatt IS NOT NULL           AS IsDiscontinued
FROM
    MakeDataSmart2026.mds.vare v

UNION ALL

SELECT
    '-1'                            AS Product_Key,
    NULL                            AS ProductID,
    'Unknown product'               AS ProductName,
    'Unknown'                       AS BrandName,
    'Unknown'                       AS ProductCategory,
    'Unknown'                       AS ProductType,
    'Unknown'                       AS Season,
 --   NULL                            AS SupplierID,
    NULL                            AS PurchaseCurrencyCode,
    NULL                            AS UnitCost,
    NULL                            AS ListPriceNOK,
    NULL                            AS LaunchDate,
    NULL                            AS DiscontinuedDate,
    false                           AS IsDiscontinued;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Product IS
'One row per product, plus Product_Key ''-1'' for unknown product. Join to Fact_GeneralLedger, Fact_SalesOrders and Bridge_MultidimensionalBridge on Product_Key.';
