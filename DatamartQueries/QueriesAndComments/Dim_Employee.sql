CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Employee AS
SELECT
    a.ansattnr                      AS Employee_Key,
    a.ansattnr                      AS EmployeeID,
    trim(a.navn)                    AS EmployeeName,
    a.firma                         AS CompanyID,
    a.avdeling                      AS Department,
    a.stilling                      AS JobTitle,
    a.brukerid                      AS UserID,
    a.ansatt_dato                   AS HireDate,
    a.slutt_dato                    AS TerminationDate,
    a.slutt_dato IS NULL            AS IsEmployed,
    a.mnd_lonn                      AS MonthlySalary,
    a.valuta                        AS SalaryCurrencyCode,
    a.bankkonto                     AS BankAccountNo
FROM
    MakeDataSmart2026.mds.ansatt a;

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Employee IS
'One row per employee. Join to Fact_Payroll on Employee_Key. UserID joins Dim_User.User_Key for employees with an ERP user.';
