CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Dim_User AS
SELECT
    b.brukerid                      AS User_Key,
    b.brukerid                      AS UserID,
    trim(b.navn)                    AS UserName,
    b.brukertype                    AS UserType,
    b.firma                         AS CompanyID,
    b.avdeling                      AS Department,
    b.stilling                      AS JobTitle,
    b.epost                         AS Email,
    b.opprettet                     AS CreatedDate,
    b.deaktivert                    AS DeactivatedDate,
    b.deaktivert IS NULL            AS IsActive
FROM
    MakeDataSmart2026.mds.bruker b;
