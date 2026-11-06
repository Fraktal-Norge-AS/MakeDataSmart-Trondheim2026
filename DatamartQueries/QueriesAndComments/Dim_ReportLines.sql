CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_ReportLines AS
WITH report_lines AS (
    SELECT
        concat_ws('.', l.rapport, l.linje)            AS report_line_key,
        l.rapport                                     AS report_id,
        r.rapportnavn                                 AS report_name,
        l.linje                                       AS report_line_id,
        trim(l.linjenavn)                             AS report_line_name,
        l.linjetype                                   AS line_type,
        l.sortering                                   AS line_sort_order,
        l.fortegn                                     AS sign_factor,
        -- Total that is not part of any other total = grand total (e.g. NET, TEL)
        l.linjetype = 'total' AND NOT EXISTS (
            SELECT 1
            FROM MakeDataSmart2026.mds.rapportsum s
            WHERE s.rapport = l.rapport
              AND s.linje = l.linje
        )                                             AS is_grand_total,
        dense_rank() OVER (ORDER BY l.rapport)        AS report_sort,
        -- Same name in several reports (e.g. EBITDA): number them so the name can be made unique
        row_number() OVER (
            PARTITION BY trim(l.linjenavn)
            ORDER BY l.rapport, l.sortering
        )                                             AS name_rank
    FROM
        MakeDataSmart2026.mds.rapportlinje l
    INNER JOIN
        MakeDataSmart2026.mds.rapport r
            ON r.rapport = l.rapport
),
styled AS (
    SELECT
        rl.report_line_key                            AS report_line_key,
        rl.report_id                                  AS report_id,
        rl.report_name                                AS report_name,
        rl.report_line_id                             AS report_line_id,
        rl.report_line_name                           AS report_line_name,
        -- Invisible word joiners (U+2060) make repeated names unique for "Sort by column" in Power BI
        rl.report_line_name || repeat(chr(8288), rl.name_rank - 1) AS sortable_report_line_name,
        rl.line_type                                  AS line_type,
        rl.line_sort_order                            AS line_sort_order,
        rl.report_sort * 1000000 + rl.line_sort_order AS sort_order,
        rl.sign_factor                                AS sign_factor,
        CASE
            WHEN rl.line_type = 'header'              THEN 'custom2'
            WHEN rl.is_grand_total                    THEN 'stylesTotal overline underline'
            WHEN rl.line_type = 'total'               THEN 'stylesSubtotal overline'
            ELSE 'normal'
        END                                           AS style,
        '#,#'                                         AS format_string
    FROM
        report_lines rl
)
SELECT
    s.report_line_key                                 AS ReportLine_Key,
    s.report_id                                       AS ReportID,
    s.report_name                                     AS ReportName,
    s.report_line_id                                  AS ReportLineID,
    s.sortable_report_line_name                       AS ReportLineName,
    s.line_type                                       AS LineType,
    s.line_sort_order                                 AS ReportLineSortOrder,
    s.sort_order                                      AS SortOrder,
    s.sign_factor                                     AS SignFactor,
    s.style                                           AS Style,
    s.format_string                                   AS FormatString,
    json_object(
        'id',           s.report_line_id,
        'displayName',  s.sortable_report_line_name,
        'formula',      '',
        'style',        s.style,
        'formatString', NULL,
        'signFactor',   NULL
    )                                                 AS JSONstyle
FROM
    styled s;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_ReportLines IS
'Report lines for the reports PL (profit and loss), BS (balance sheet) and MGMT (management P&L), one row per line. Join to Bridge_ReportLineHierarchy on ReportLine_Key. Path to the amounts: Dim_ReportLines -> Bridge_ReportLineHierarchy -> Bridge_MultidimensionalBridge -> Fact_GeneralLedger. Sort lines by SortOrder.';
