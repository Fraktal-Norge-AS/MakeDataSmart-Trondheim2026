CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart.Dim_Account AS
SELECT
    k.kontonr                                       AS Account_Key,
    k.kontonr                                       AS AccountID,
    k.kontonavn                                     AS AccountName,
    concat_ws(' ', k.kontonr, k.kontonavn)          AS AccountDisplayName,
    k.kontoklasse                                   AS AccountClass,
    k.kontogruppe                                   AS AccountGroup,
    k.rapporttype                                   AS AccountType
FROM
    MakeDataSmart2026.mds.kontoplan k;
