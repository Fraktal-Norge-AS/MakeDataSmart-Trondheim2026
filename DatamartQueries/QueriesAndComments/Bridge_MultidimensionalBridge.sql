CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Bridge_MultidimensionalBridge AS
WITH line_mapping AS (
    -- One row per mapping rule (only base lines have rules; totals are in rapportsum)
    SELECT
        concat_ws('.', o.rapport, o.linje)            AS report_line_id,
        o.fra_konto                                   AS account_from,
        o.til_konto                                   AS account_to,
        o.firma                                       AS company_id,
        o.varegruppe                                  AS product_category
    FROM
        MakeDataSmart2026.mds.rapportoppsett o
),
accounts_per_line AS (
    -- Every account in the chart of accounts within the range
    SELECT
        m.report_line_id                              AS report_line_id,
        k.kontonr                                     AS account_id,
        m.company_id                                  AS company_id,
        m.product_category                            AS product_category
    FROM
        line_mapping m
    INNER JOIN
        MakeDataSmart2026.mds.kontoplan k
            ON k.kontonr BETWEEN m.account_from AND m.account_to
)
SELECT DISTINCT
    a.report_line_id                                  AS ReportLine_Key,
    a.account_id                                      AS Account_Key,
    COALESCE(v.varenr, '-999')                        AS Product_Key,     -- -999 = no product filter
    COALESCE(a.company_id, '-999')                    AS Company_Key,     -- -999 = no company filter
    CASE
        WHEN a.product_category IS NULL     AND a.company_id IS NULL     THEN 'A'
        WHEN a.product_category IS NOT NULL AND a.company_id IS NULL     THEN 'AP'
        WHEN a.product_category IS NULL     AND a.company_id IS NOT NULL THEN 'AC'
        ELSE 'APC'
    END                                               AS FilterCase
FROM
    accounts_per_line a
LEFT JOIN
    MakeDataSmart2026.mds.vare v
        ON v.varegruppe = a.product_category;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Bridge_MultidimensionalBridge IS
'Maps base report lines to the general ledger. Join to Fact_GeneralLedger on Account_Key, and also on Product_Key and Company_Key unless they are ''-999'' (= no filter; FilterCase A, AP, AC or APC tells which keys apply). Then join ReportLine_Key to Bridge_ReportLineHierarchy.BridgeReportLine_Key to get totals.';
