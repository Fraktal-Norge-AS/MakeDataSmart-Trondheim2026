CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Date AS
WITH
easter AS (
    -- Easter Sunday per year
    SELECT 
      y, make_date(y, n // 31, n % 31 + 1) AS EasterSunday
    FROM (
        SELECT y,
            y % 19 AS a, y // 100 AS b, y % 100 AS c,
            b // 4 AS d, b % 4 AS e, (b + 8) // 25 AS f,
            (b - f + 1) // 3 AS g,
            (19 * a + b - d - g + 15) % 30 AS h, c // 4 AS i, c % 4 AS k,
            (32 + 2 * e + 2 * i - h - k) % 7 AS l,
            (a + 11 * h + 22 * l) // 451 AS m,
            h + l - 7 * m + 114 AS n
        FROM range(2005, 2030) t(y)
    )
),
holidays AS (
    -- Norwegian public holidays
    SELECT
        COALESCE(e.EasterSunday + h.EasterOffset, make_date(e.y, h.Mon, h.DayNo)) AS HolidayDate,
        h.HolidayName
    FROM 
      easter e
    CROSS JOIN (VALUES
        (1,    1,    NULL, '1. nyttårsdag'),
        (NULL, NULL, -3,   'Skjærtorsdag'),
        (NULL, NULL, -2,   'Langfredag'),
        (NULL, NULL, 0,    '1. påskedag'),
        (NULL, NULL, 1,    '2. påskedag'),
        (5,    1,    NULL, 'Arbeidernes dag'),
        (5,    17,   NULL, 'Grunnlovsdag'),
        (NULL, NULL, 39,   'Kristi himmelfartsdag'),
        (NULL, NULL, 49,   '1. pinsedag'),
        (NULL, NULL, 50,   '2. pinsedag'),
        (12,   25,   NULL, '1. juledag'),
        (12,   26,   NULL, '2. juledag')
    ) h (Mon, DayNo, EasterOffset, HolidayName)
),
holiday_per_date AS (
    SELECT 
      HolidayDate, 
      string_agg(HolidayName, '/' ORDER BY HolidayName) AS HolidayName
    FROM 
      holidays
    GROUP BY 
      HolidayDate
),
dates AS (
    SELECT 
      CAST(range AS DATE) AS d
    FROM 
      range(DATE '2023-01-01', DATE '2027-01-01', INTERVAL 1 DAY)
)
SELECT
    d                                                   AS Date_Key,
    d                                                   AS "Date",
    strftime(d, '%B')                                   AS MonthName,
    strftime(d, '%Y %m')                                AS YearMonth,
    dayname(d)                                          AS WeekdayName,
    -- Like SQL Server DATEPART(WEEK): week 1 holds 1 January, new week each Sunday
    lpad(CAST((dayofyear(d) + dayofweek(make_date(year(d), 1, 1)) - 1) // 7 + 1 AS VARCHAR), 2, '0') AS Week,
    year(d)                                             AS "Year",
    lpad(CAST(week(d) AS VARCHAR), 2, '0')              AS IsoWeek,
    isoyear(d)                                          AS IsoYear,
    concat_ws(' ', isoyear(d), lpad(CAST(week(d) AS VARCHAR), 2, '0')) AS IsoYearIsoWeek,
    lpad(CAST(quarter(d) AS VARCHAR), 2, '0')           AS "Quarter",
    concat_ws(' ', year(d), lpad(CAST(quarter(d) AS VARCHAR), 2, '0')) AS YearQuarter,
    row_number() OVER (ORDER BY d)                      AS DateUID,
    month(d)                                            AS MonthUID,
    dense_rank() OVER (ORDER BY year(d))                AS YearUID,
    dense_rank() OVER (ORDER BY year(d), month(d))      AS YearMonthUID,
    dense_rank() OVER (ORDER BY isoyear(d), week(d))    AS IsoYearIsoWeekUID,
    quarter(d)                                          AS QuarterUID,
    dense_rank() OVER (ORDER BY year(d), quarter(d))    AS YearQuarterUID,
    dayofyear(d)                                        AS DayOfYear,
    day(d)                                              AS DayOfMonth,
    isodow(d)                                           AS DayOfWeek,
    date_diff('day', d, current_date)                   AS DaysFromToday,
    CASE WHEN isodow(d) >= 6 THEN 'Weekend' ELSE 'Weekday' END AS DayType,
    h.HolidayName IS NOT NULL                           AS IsHoliday,
    h.HolidayName,
    date_diff('month', date_trunc('month', d), date_trunc('month', current_date)) AS MonthsFromToday
FROM 
  dates
LEFT OUTER JOIN 
  holiday_per_date h 
  ON 
    h.HolidayDate = dates.d;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Date IS
'One row per calendar day, 2023-2026, with Norwegian public holidays. Join Date_Key to the date keys in the facts: Date_Key (Fact_GeneralLedger), OrderDate_Key and RequestedDeliveryDate_Key (Fact_SalesOrders), TransactionDate_Key, InvoiceDate_Key and DueDate_Key (Fact_Subledger), PaymentDate_Key and PayPeriod_Key (Fact_Payroll).';
