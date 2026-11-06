CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Fact_SalesOrders AS
SELECT
    -- Keys
    o.firma                                           AS Company_Key,
    o.ordredato                                       AS OrderDate_Key,
    o.onsket_lev_dato                                 AS RequestedDeliveryDate_Key,
    trim(o.kundenr)                                   AS Customer_Key,
    trim(l.varenr)                                    AS Product_Key,

    -- Order attributes
    o.ordrenr                                         AS OrderID,
    o.ordre_id                                        AS OrderInternalID,
    l.linjenr                                         AS LineNo,
    o.ordretype                                       AS OrderType,
    o.status                                          AS OrderStatus,
    greatest(o.ordredato, DATE '2023-01-01')          AS ExchangeRateDate,   -- no rates before 2023 (first orders Dec 2022)

    -- Measures
    l.antall                                          AS QuantityOrdered,
    l.antall_fakt                                     AS QuantityInvoiced,
    l.antall_kans                                     AS QuantityCancelled,
    l.antall - l.antall_fakt - l.antall_kans          AS QuantityOpen,
    l.pris                                            AS UnitPrice,
    l.rabatt                                          AS DiscountPct,
    o.valuta                                          AS OrderCurrencyCode,
    l.belop                                           AS LineAmount,
    round(l.belop * (l.antall - l.antall_fakt - l.antall_kans) / NULLIF(l.antall, 0), 2) AS OpenAmount,
    round(l.belop * k.kurs, 2)                        AS LineAmountNOK
FROM
    MakeDataSmart2026.mds.ordrelinje l
JOIN
    MakeDataSmart2026.mds.ordre o
        ON o.ordre_id = l.ordre_id
LEFT JOIN
    MakeDataSmart2026.mds.valutakurs k
        ON k.valuta = o.valuta
       AND k.kursdato = greatest(o.ordredato, DATE '2023-01-01');
