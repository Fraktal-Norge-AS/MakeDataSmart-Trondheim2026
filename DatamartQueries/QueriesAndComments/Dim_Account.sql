CREATE OR REPLACE VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Account AS
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

COMMENT ON VIEW MakeDataSmart2026.mds_datamart_comments.Dim_Account IS
'Chart of accounts, one row per account. Join to Fact_GeneralLedger and Bridge_MultidimensionalBridge on Account_Key. AccountType is PL (profit and loss) or BS (balance sheet).';
