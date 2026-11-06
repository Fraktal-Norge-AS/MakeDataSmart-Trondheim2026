CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Bridge_ReportLineHierarchy AS
WITH RECURSIVE hierarchy AS (
    -- Start: every total line with its direct components
    SELECT
        s.rapport                                     AS report_id,
        s.sumlinje                                    AS report_line_id,
        s.linje                                       AS child_line_id
    FROM
        MakeDataSmart2026.mds.rapportsum s

    UNION ALL

    -- Walk down: a component that is itself a total is replaced by its components
    SELECT
        h.report_id                                   AS report_id,
        h.report_line_id                              AS report_line_id,
        s.linje                                       AS child_line_id
    FROM
        hierarchy h
    INNER JOIN
        MakeDataSmart2026.mds.rapportsum s
            ON s.rapport = h.report_id
           AND s.sumlinje = h.child_line_id
),
base_lines AS (
    SELECT
        l.rapport                                     AS report_id,
        l.linje                                       AS report_line_id,
        COALESCE(l.fortegn, 1)                        AS sign_factor
    FROM
        MakeDataSmart2026.mds.rapportlinje l
    WHERE
        l.linjetype = 'mapped'
),
total_lines AS (
    -- Totals resolved down to base lines; the base line's sign is applied
    -- (rapportsum has no signs of its own, every component is added)
    SELECT
        concat_ws('.', h.report_id, h.report_line_id) AS report_line_key,
        concat_ws('.', b.report_id, b.report_line_id) AS bridge_report_line_key,
        SUM(b.sign_factor)                            AS sign_factor
    FROM
        hierarchy h
    INNER JOIN
        base_lines b
            ON b.report_id = h.report_id
           AND b.report_line_id = h.child_line_id
    GROUP BY
        h.report_id,
        h.report_line_id,
        b.report_id,
        b.report_line_id
)
SELECT
    t.report_line_key                                 AS ReportLine_Key,
    t.bridge_report_line_key                          AS BridgeReportLine_Key,
    t.sign_factor                                     AS SignFactor
FROM
    total_lines t

UNION ALL

-- Base lines point to themselves
SELECT
    concat_ws('.', b.report_id, b.report_line_id)     AS ReportLine_Key,
    concat_ws('.', b.report_id, b.report_line_id)     AS BridgeReportLine_Key,
    b.sign_factor                                     AS SignFactor
FROM
    base_lines b;
