CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Dim_Employee AS
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
    MakeDataSmart2026.mds.ansatt a
  
