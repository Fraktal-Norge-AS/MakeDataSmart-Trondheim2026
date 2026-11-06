CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Company AS
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

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Company IS
'One row per company in the group. Join to all facts on Company_Key. In Fact_GeneralLedger and Fact_Subledger, InterCompany_Key also joins here (the counterparty group company).';
