CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Dim_Company AS
SELECT
    f.firma                         AS Company_Key,
    f.firma                         as CompanyID,
    f.firmanavn                     AS CompanyName,
    f.landkode                      AS CountryCode,
    f.land                          AS Country,
    f.sted                          AS City,
    f.valuta                        AS CompanyCurrencyCode,
    f.hovedkontor                   AS IsMainOffice,
    CASE 
        WHEN f.hovedkontor THEN 'Parent' 
        ELSE 'Subsidiary'
        END                         AS CompanyType
FROM 
    MakeDataSmart2026.mds.firma f;
