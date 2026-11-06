"""
Names and word lists used by fill_company_data.py.

Handwritten parody names are for the companies people will actually see in the
demo (big customers, main brands, service vendors). The long tail is generated
from the per-country word lists below and is deliberately boring.

Rule: negative demo stories (bad debt, suspicious supplier, ...) only ever use
obviously invented names, never parodies of real companies.
"""

# --------------------------------------------------------------------------
# Per-country word lists and name templates
# --------------------------------------------------------------------------
LOCALE = {
    "NO": dict(
        cities=["Oslo", "Bergen", "Trondheim", "Stavanger", "Tromsø", "Kristiansand",
                "Drammen", "Fredrikstad", "Bodø", "Ålesund", "Lillehammer", "Hamar",
                "Molde", "Harstad", "Tønsberg", "Sandefjord", "Skien", "Gjøvik",
                "Narvik", "Alta", "Geilo", "Hemsedal", "Voss", "Sogndal", "Røros",
                "Kongsberg", "Arendal", "Haugesund", "Steinkjer", "Mo i Rana"],
        surnames=["Hansen", "Johansen", "Olsen", "Larsen", "Andersen", "Pedersen",
                  "Nilsen", "Kristiansen", "Jensen", "Karlsen", "Johnsen", "Pettersen",
                  "Eriksen", "Berg", "Haugen", "Hagen", "Johannessen", "Andreassen",
                  "Jacobsen", "Dahl", "Lund", "Halvorsen", "Bakken", "Solberg", "Strand"],
        nature=["Fjell", "Tind", "Vidde", "Fjord", "Bre", "Skog", "Elv", "Topp",
                "Varde", "Kyst", "Høyfjell", "Nord"],
        retail=["{surname} Sport AS", "{city} Sport AS", "Sportshuset {city} AS",
                "{nature} & Fritid AS", "{nature}sport {city} AS", "{city} Friluft AS",
                "Tur & Telt {city} AS", "{surname}s Sykkel og Sport AS",
                "{surname} Sport {city} AS", "{surname}s Fritid {city} AS"],
        gear=["shop", "utstyr", "sport", "tur", "ski", "sykkel", "telt", "sko"],
        webshop=["{nature_lc}{gear}.no AS", "billig{nature_lc}.no AS"],
        services={
            "Rent":                  ["{city} Næringseiendom AS", "{surname} Eiendom AS"],
            "Facility services":     ["Rent & Pent {city} AS", "{surname} Renhold AS"],
            "Utilities":             ["{city} Energi AS"],
            "Equipment & furniture": ["{surname} Kontormøbler AS"],
            "Consulting & audit":    ["Advokatfirma {surname} & {surname2} AS",
                                      "{surname} Revisjon AS", "{surname} Regnskap AS"],
            "Office supplies":       ["{city} Kontorrekvisita AS"],
            "Telecom & IT":          ["{surname} Data AS", "{nature} IT AS"],
            "Vehicles":              ["{surname} Bil AS", "{city} Bilverksted AS"],
            "Travel":                ["{city} Hotell AS", "{nature} Reiser AS"],
            "Marketing":             ["Reklamebyrået {nature} AS", "{surname} Kommunikasjon AS"],
            "Events":                ["{city} Messe og Event AS"],
            "Freight":               ["{surname} Transport AS", "{city} Budservice AS"],
        },
    ),
    "SE": dict(
        cities=["Stockholm", "Göteborg", "Malmö", "Uppsala", "Västerås", "Örebro",
                "Linköping", "Helsingborg", "Jönköping", "Norrköping", "Lund", "Umeå",
                "Gävle", "Borås", "Sundsvall", "Luleå", "Östersund", "Kiruna", "Åre",
                "Sälen", "Falun", "Karlstad", "Växjö", "Visby", "Skellefteå"],
        surnames=["Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson",
                  "Olsson", "Persson", "Svensson", "Gustafsson", "Pettersson", "Jonsson",
                  "Lindberg", "Lindqvist", "Berglund", "Lundgren", "Holm", "Bergström",
                  "Sandberg", "Ek"],
        nature=["Fjäll", "Skog", "Sjö", "Älv", "Berg", "Topp", "Kust", "Myr", "Norr",
                "Vildmark"],
        retail=["{surname}s Sport AB", "{city} Sport AB", "Sporthuset {city} AB",
                "{nature} & Fritid AB", "{nature}sport {city} AB", "{city} Friluftsbutik AB",
                "Cykel & Sport {city} AB", "{surname}s Sport {city} AB",
                "{nature} & Fritid {city} AB"],
        gear=["shop", "utrustning", "sport", "tur", "skidor", "cykel", "tält", "skor"],
        webshop=["{nature_lc}{gear}.se AB"],
        services={
            "Rent":                  ["{city} Fastigheter AB", "{surname}s Fastighets AB"],
            "Facility services":     ["{surname}s Städ AB"],
            "Utilities":             ["{city} Energi AB"],
            "Equipment & furniture": ["{surname}s Kontorsmöbler AB"],
            "Consulting & audit":    ["Advokatfirman {surname} & {surname2} AB",
                                      "{surname} Revision AB"],
            "Office supplies":       ["{city} Kontorsmaterial AB"],
            "Telecom & IT":          ["{surname} Data AB", "{nature} IT AB"],
            "Vehicles":              ["{surname}s Bil AB"],
            "Travel":                ["Hotell {city} AB", "{nature} Resor AB"],
            "Marketing":             ["Reklambyrån {nature} AB"],
            "Events":                ["{city} Mässa & Event AB"],
            "Freight":               ["{surname}s Åkeri AB"],
        },
    ),
    "DK": dict(
        cities=["København", "Aarhus", "Odense", "Aalborg", "Esbjerg", "Randers", "Kolding",
                "Horsens", "Vejle", "Roskilde", "Herning", "Silkeborg", "Næstved",
                "Fredericia", "Viborg", "Skagen", "Svendborg", "Holstebro", "Hillerød",
                "Helsingør"],
        surnames=["Nielsen", "Jensen", "Hansen", "Pedersen", "Andersen", "Christensen",
                  "Larsen", "Sørensen", "Rasmussen", "Jørgensen", "Petersen", "Madsen",
                  "Kristensen", "Olsen", "Thomsen", "Poulsen", "Møller", "Mortensen"],
        nature=["Klit", "Skov", "Strand", "Fjord", "Bakke", "Hede", "Sø", "Kyst", "Vind",
                "Bølge"],
        retail=["{surname}s Sport ApS", "{city} Sport ApS", "Sportshuset {city} ApS",
                "{nature} & Fritid ApS", "{nature}sport {city} ApS", "{city} Friluft ApS",
                "Cykel & Sport {city} ApS", "{surname}s Sport {city} ApS",
                "{nature} & Fritid {city} ApS"],
        gear=["shop", "udstyr", "sport", "tur", "ski", "cykel", "telt", "sko"],
        webshop=["{nature_lc}{gear}.dk ApS"],
        services={
            "Rent":                  ["{city} Erhvervsejendomme ApS"],
            "Facility services":     ["{surname}s Rengøring ApS"],
            "Utilities":             ["{city} Forsyning A/S"],
            "Equipment & furniture": ["{surname} Kontormøbler ApS"],
            "Consulting & audit":    ["Advokatfirmaet {surname} & {surname2}",
                                      "{surname} Revision ApS"],
            "Office supplies":       ["{city} Kontorartikler ApS"],
            "Telecom & IT":          ["{surname} IT ApS"],
            "Vehicles":              ["{surname}s Auto ApS"],
            "Travel":                ["Hotel {city} ApS"],
            "Marketing":             ["Reklamebureauet {nature} ApS"],
            "Events":                ["{city} Messe & Event ApS"],
            "Freight":               ["{surname}s Vognmandsforretning ApS"],
        },
    ),
    "FI": dict(
        cities=["Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu", "Turku", "Jyväskylä",
                "Lahti", "Kuopio", "Pori", "Joensuu", "Lappeenranta", "Hämeenlinna",
                "Vaasa", "Rovaniemi", "Seinäjoki", "Kajaani", "Levi", "Ruka", "Kittilä"],
        surnames=["Korhonen", "Virtanen", "Mäkinen", "Nieminen", "Mäkelä", "Hämäläinen",
                  "Laine", "Heikkinen", "Koskinen", "Järvinen", "Lehtonen", "Lehtinen",
                  "Saarinen", "Salminen", "Heinonen", "Niemi", "Kinnunen"],
        nature=["Tunturi", "Metsä", "Järvi", "Erä", "Revontuli", "Kallio", "Koski", "Saari",
                "Lumi", "Karhu"],
        retail=["{surname} Sport Oy", "Urheilu-{surname} Oy", "{nature} Sport Oy",
                "Retki-{surname} Oy", "Sport {city} Oy", "{city} Outdoor Oy",
                "Pyörä-{surname} Oy", "{surname} Sport {city} Oy", "{nature} Outdoor {city} Oy"],
        gear=["kauppa", "shop", "urheilu", "retki", "hiihto", "pyörä", "teltta", "kenkä"],
        webshop=["{nature_lc}{gear}.fi Oy"],
        services={
            "Rent":                  ["Kiinteistö {surname} Oy"],
            "Facility services":     ["Siivous {surname} Oy"],
            "Utilities":             ["Sähkö-{surname} Oy"],
            "Equipment & furniture": ["Kalustetalo {surname} Oy"],
            "Consulting & audit":    ["Asianajotoimisto {surname} & {surname2}",
                                      "Tilintarkastus {surname} Oy"],
            "Office supplies":       ["Toimistotarvike {surname} Oy"],
            "Telecom & IT":          ["IT-{surname} Oy"],
            "Vehicles":              ["Auto-{surname} Oy"],
            "Travel":                ["Hotelli {nature} Oy"],
            "Marketing":             ["Mainostoimisto {nature} Oy"],
            "Events":                ["Tapahtuma {nature} Oy"],
            "Freight":               ["Kuljetus {surname} Oy"],
        },
    ),
    "DE": dict(
        cities=["Hamburg", "Berlin", "München", "Köln", "Frankfurt", "Stuttgart",
                "Düsseldorf", "Leipzig", "Dresden", "Hannover", "Nürnberg", "Bremen",
                "Freiburg", "Garmisch-Partenkirchen", "Berchtesgaden", "Kiel", "Rostock",
                "Augsburg", "Regensburg", "Kempten"],
        surnames=["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner",
                  "Becker", "Schulz", "Hoffmann", "Koch", "Bauer", "Richter", "Klein",
                  "Wolf", "Schröder", "Neumann", "Schwarz"],
        nature=["Berg", "Wald", "Gipfel", "Alpen", "Fels", "Tal", "Heide", "Nord", "Wander",
                "Kletter"],
        retail=["Sport {surname} GmbH", "Sporthaus {surname} GmbH", "{nature}sport {city} GmbH",
                "{nature} & Freizeit GmbH", "Outdoor {surname} GmbH", "Radsport {surname} GmbH",
                "Sport {surname} {city} GmbH", "{nature}sport {surname} GmbH"],
        gear=["shop", "ausruestung", "sport", "tour", "ski", "rad", "zelt", "schuh"],
        webshop=["{nature_lc}{gear}.de GmbH"],
        services={
            "Rent":                  ["Immobilien {surname} GmbH"],
            "Facility services":     ["{surname} Gebäudereinigung GmbH"],
            "Utilities":             ["Stadtwerke {city} GmbH"],
            "Equipment & furniture": ["Büromöbel {surname} GmbH"],
            "Consulting & audit":    ["Kanzlei {surname} & {surname2}",
                                      "{surname} Steuerberatung GmbH"],
            "Office supplies":       ["Bürobedarf {city} GmbH"],
            "Telecom & IT":          ["{surname} IT-Service GmbH"],
            "Vehicles":              ["Autohaus {surname} GmbH"],
            "Travel":                ["Hotel {nature}blick GmbH"],
            "Marketing":             ["Werbeagentur {nature} GmbH"],
            "Events":                ["{city} Messe & Event GmbH"],
            "Freight":               ["Spedition {surname} GmbH"],
        },
    ),
}

LEGAL_SUFFIX = {"NO": "AS", "SE": "AB", "DK": "ApS", "FI": "Oy", "DE": "GmbH"}

# First names for generated employees (surnames come from LOCALE)
FIRST_NAMES = {
    "NO": ["Ole", "Kari", "Lars", "Ingrid", "Anders", "Marte", "Jonas", "Silje", "Erik", "Hanne",
           "Thomas", "Ida", "Martin", "Nora", "Kristian", "Emma", "Even", "Tone", "Sindre", "Maria",
           "Magnus", "Linn", "Håkon", "Camilla", "Vegard", "Sigrid", "Jørgen", "Astrid"],
    "SE": ["Erik", "Anna", "Lars", "Maria", "Johan", "Karin", "Anders", "Emma", "Oskar", "Sara",
           "Gustav", "Elin", "Fredrik", "Linnea", "Henrik", "Ebba", "Mattias", "Frida", "Viktor",
           "Malin", "Nils", "Klara", "Axel", "Ida", "Jonas", "Maja"],
    "DK": ["Mads", "Mette", "Jens", "Anne", "Søren", "Camilla", "Rasmus", "Louise", "Mikkel",
           "Sofie", "Henrik", "Line", "Thomas", "Julie", "Kasper", "Maja", "Christian", "Ida",
           "Anders", "Katrine", "Frederik", "Signe", "Jakob", "Emma", "Nikolaj"],
    "FI": ["Mikko", "Anna", "Juha", "Laura", "Antti", "Johanna", "Ville", "Maria", "Teemu", "Elina",
           "Jussi", "Sanna", "Pekka", "Noora", "Matti", "Kaisa", "Janne", "Aino", "Lauri", "Heidi",
           "Tuomas", "Emilia", "Sami", "Riikka", "Olli"],
    "DE": ["Thomas", "Anna", "Michael", "Julia", "Stefan", "Laura", "Andreas", "Katrin", "Jan",
           "Lena", "Markus", "Sarah", "Tobias", "Lisa", "Florian", "Sandra", "Daniel", "Nina",
           "Christian", "Jana", "Sebastian", "Miriam", "Lukas", "Sabine", "Felix"],
}

# --------------------------------------------------------------------------
# ERP users (handwritten)
# --------------------------------------------------------------------------
# (user_id, full name, entity_id, department, job title, created, deactivated)
# Created/deactivated are (y, m, d) or None. A few joined or left during the period.
USERS = [
    # Norway (HQ)
    ("ingridm",  "Ingrid Moen",           "NO01", "Management", "CFO",                    (2014, 3, 1),  None),
    ("torej",    "Tore Johnsen",          "NO01", "Finance",    "Group financial controller", (2016, 8, 15), None),
    ("rogerb",   "Roger Bakke",           "NO01", "Finance",    "Accountant",             (2019, 8, 12), None),  # story candidate: the one to blame
    ("sissels",  "Sissel Strand",         "NO01", "Finance",    "Accountant",             (2012, 1, 9),  None),
    ("kamillah", "Kamilla Haugen",        "NO01", "Finance",    "Accounts payable clerk", (2021, 4, 6),  None),
    ("eirikd",   "Eirik Dahl",            "NO01", "Finance",    "Accounts receivable clerk", (2018, 10, 1), (2024, 5, 31)),
    ("noorab",   "Noora Berg",            "NO01", "Finance",    "Accounts receivable clerk", (2024, 6, 3),  None),
    ("haraldl",  "Harald Lund",           "NO01", "Finance",    "Payroll officer",        (2010, 2, 1),  None),
    ("mortens",  "Morten Solberg",        "NO01", "Sales",      "Key account manager",    (2013, 5, 2),  None),
    ("linap",    "Lina Pettersen",        "NO01", "Sales",      "Sales coordinator",      (2020, 9, 1),  None),
    ("kjetilh",  "Kjetil Halvorsen",      "NO01", "Purchasing", "Purchasing manager",     (2011, 11, 14), None),
    ("aslaugn",  "Aslaug Nilsen",         "NO01", "Purchasing", "Buyer",                  (2022, 2, 21), None),
    ("petterk",  "Petter Karlsen",        "NO01", "Logistics",  "Warehouse manager",      (2015, 6, 8),  None),
    ("andreasj", "Andreas Jacobsen",      "NO01", "IT",         "ERP administrator",      (2017, 3, 20), None),
    # Sweden
    ("annal",    "Anna Lindqvist",        "SE01", "Finance",    "Finance manager",        (2015, 1, 12), None),
    ("johane",   "Johan Eriksson",        "SE01", "Finance",    "Accountant",             (2019, 3, 4),  None),
    ("elinb",    "Elin Berglund",         "SE01", "Finance",    "Accounts payable clerk", (2021, 8, 16), None),
    ("mikaelh",  "Mikael Holm",           "SE01", "Sales",      "Sales manager",          (2016, 4, 1),  None),
    ("saran",    "Sara Nilsson",          "SE01", "Purchasing", "Buyer",                  (2023, 9, 4),  None),
    # Denmark
    ("mettej",   "Mette Jørgensen",       "DK01", "Finance",    "Finance manager",        (2017, 2, 1),  None),
    ("rasmusm",  "Rasmus Madsen",         "DK01", "Finance",    "Accountant",             (2020, 1, 6),  (2025, 2, 28)),
    ("idak",     "Ida Kristensen",        "DK01", "Finance",    "Accountant",             (2025, 3, 3),  None),
    ("larsn",    "Lars Nielsen",          "DK01", "Sales",      "Sales manager",          (2018, 5, 14), None),
    # Finland
    ("liisak",   "Liisa Korhonen",        "FI01", "Finance",    "Finance manager",        (2016, 10, 3), None),
    ("mattiv",   "Matti Virtanen",        "FI01", "Finance",    "Accountant",             (2019, 11, 11), None),
    ("annem",    "Anne Mäkinen",          "FI01", "Sales",      "Sales manager",          (2021, 1, 18), None),
    # Germany
    ("katrins",  "Katrin Schmidt",        "DE01", "Finance",    "Finance manager",        (2018, 7, 2),  None),
    ("thomasw",  "Thomas Weber",          "DE01", "Finance",    "Accountant",             (2020, 4, 15), None),
    ("julias",   "Julia Schneider",       "DE01", "Finance",    "Accounts payable clerk", (2023, 2, 1),  None),
    ("stefanm",  "Stefan Müller",         "DE01", "Sales",      "Sales manager",          (2019, 9, 2),  None),
]

# Story: Roger books private weekend trips as travel expenses.
# (ledger description, currency, season: Winter = Dec-Apr, Summer = May-Sep, Any,
#  price range in NOK before the yearly escalation)
# Descriptions are meant to be a bit obvious. No real businesses.
ROGER_TRIPS = [
    ("Weekend Hemsedal - ski w/ family",            "NOK", "Winter",  6_000, 14_000),
    ("Cabin rental Hafjell, private",               "NOK", "Winter",  5_000, 12_000),
    ("Ski pass Trysil x4 (kids + wife)",            "NOK", "Winter",  2_500,  4_500),
    ("Hotel Geilo 2 nights - family weekend",       "NOK", "Winter",  4_000,  9_000),
    ("Apres-ski dinner Hemsedal, private",          "NOK", "Winter",  1_500,  4_000),
    ("Ski trip Åre - hotel + lift pass, R.B.",      "SEK", "Winter",  7_000, 15_000),
    ("Weekend Copenhagen w/ wife - hotel",          "DKK", "Any",     4_000,  9_000),
    ("Spa weekend Son - R.B. + wife",               "NOK", "Any",     3_500,  8_000),
    ("Hotel Bergen - wife's birthday",              "NOK", "Any",     3_000,  7_000),
    ("Dinner private celebration, 8 pers",          "NOK", "Any",     4_000,  9_000),
    ("Taxi Gardermoen - private",                   "NOK", "Any",       700,  1_400),
    ("Concert tickets + hotel Oslo, private",       "NOK", "Any",     3_000,  6_000),
    ("Flights OSL-ALC private",                     "NOK", "Any",     3_000,  8_000),
    ("Hotel Alicante 2 nights (wife's birthday)",   "EUR", "Any",     3_500,  7_000),
    ("City break Berlin - hotel + dinner, private", "EUR", "Any",     5_000, 11_000),
    ("Football weekend London - tickets + hotel",   "GBP", "Any",     8_000, 16_000),
    ("Golf trip Marbella - green fees",             "EUR", "Summer",  3_000,  6_000),
    ("Golf weekend Marbella - hotel, private",      "EUR", "Summer",  7_000, 15_000),
    ("Boat rental Tjøme, family weekend",           "NOK", "Summer",  3_000,  7_000),
    ("Cabin rental Lofoten - summer holiday",       "NOK", "Summer",  8_000, 18_000),
    ("Weekend Mallorca - family, flights",          "EUR", "Summer",  8_000, 18_000),
    ("Hotel Kristiansand + zoo tickets (kids)",     "NOK", "Summer",  4_000,  8_000),
    ("Wine tasting weekend Bordeaux, private",      "EUR", "Summer",  9_000, 18_000),
    ("Music festival weekend - tickets x2",         "NOK", "Summer",  3_500,  6_000),
]

# Integration accounts that post automatically (no person behind them).
# (user_id, description, entity_id or None for group-wide, created)
SYSTEM_USERS = [
    ("SYS_ORDER",   "Order-to-invoice integration",   None, (2016, 1, 1)),
    ("SYS_WEBSHOP", "Webshop order import",           None, (2019, 4, 1)),
    ("SYS_EDI",     "EDI supplier invoice import",    None, (2016, 1, 1)),
    ("SYS_BANK",    "Bank statement import",          None, (2016, 1, 1)),
    ("SYS_PAYROLL", "Payroll system integration",     None, (2016, 1, 1)),
    ("SYS_CLOSE",   "Period-end batch jobs (depreciation, accruals, FX)", None, (2016, 1, 1)),
    ("SYS_SPECORD", "Special order configurator integration", None, (2022, 9, 1)),   # story: buggy
]

# Handpicked duplicates of well-known customers: (original name, duplicate
# name, variation, customer_since of the duplicate (y, m, d))
HANDPICKED_DUPLICATES = [
    ("XXXL Sport & Villmark AS", "XXXL SPORT & VILLMARK AS", "upper case", (2024, 9, 16)),
    ("Sport 1½ AS", "Sport​ 1½ AS", "invisible zero-width space (U+200B) after 'Sport'",
     (2025, 2, 3)),
]

# Story: Roger's shell supplier, added at the end of the supplier list
# (name, type, category, brand, country, currency, terms, account, entity)
SHELL_SUPPLIERS = [
    ("Bakke Rådgivning ENK", "Services", "Consulting & audit", None, "NO", "NOK", 14, 6700, "NO01"),
]
SMALL_BRAND_WORDS = ["Gear", "Outdoor", "Design", "Equipment", "Works", "Supply"]

# --------------------------------------------------------------------------
# Customers (handwritten)
# --------------------------------------------------------------------------
# (entity_id, name, segment, city, customer since: year or (y, m, d))
PUN_CUSTOMERS = [
    # Norway
    ("NO01", "XXXL Sport & Villmark AS",          "Key account",      "Oslo",        2008),
    ("NO01", "Intersnort Norge AS",                "Chain store",      "Oslo",        2005),
    ("NO01", "Sport 1½ AS",                        "Chain store",      "Lillehammer", 2010),
    ("NO01", "Antons Spurt AS",                    "Chain store",      "Oslo",        2011),
    ("NO01", "Klas Oldson AS",                     "Chain store",      "Oslo",        2013),
    ("NO01", "Biltemu Norge AS",                   "Chain store",      "Drammen",     2016),
    ("NO01", "Tørrshov Sport AS",                  "Independent",      "Oslo",        2009),
    ("NO01", "Oslo Sportslagret AS",               "Independent",      "Oslo",        2012),
    ("NO01", "Fjellsprett.no AS",                  "Webshop",          "Bergen",      2017),
    ("NO01", "Inkomplett.no AS",                   "Webshop",          "Sandefjord",  2015),
    ("NO01", "Milsnurrer AS",                      "Webshop",          "Oslo",        2019),
    ("NO01", "Ut på Tur, Aldri Sur AS",            "Independent",      "Lillehammer", 2014),
    ("NO01", "Det Finnes Ikke Dårlig Vær AS",      "Independent",      "Bergen",      2011),
    ("NO01", "Påskefjellet AS",                    "Independent",      "Geilo",       2016),
    ("NO01", "Smøreboden AS",                      "Independent",      "Trondheim",   2010),
    ("NO01", "Brødskive & Bålkaffe AS",            "Independent",      "Tromsø",      2018),
    ("NO01", "Konkurs & Sønn Sport AS",            "Chain store",      "Bergen",      2012),  # story candidate
    ("NO01", "Online consumers (nordvidde.no)",    "Online consumers", "Oslo",        2019),
    # Sweden
    ("SE01", "Podium Sport AB",                    "Key account",      "Stockholm",   2007),
    ("SE01", "Intersnort Sverige AB",              "Chain store",      "Stockholm",   2006),
    ("SE01", "Team Sportig AB",                    "Chain store",      "Göteborg",    2012),
    ("SE01", "Naturkompisen AB",                   "Chain store",      "Stockholm",   2010),
    ("SE01", "Klas Oldson AB",                     "Chain store",      "Stockholm",   2013),
    ("SE01", "Biltemu Sverige AB",                 "Chain store",      "Helsingborg", 2016),
    ("SE01", "Outsouth AB",                        "Webshop",          "Göteborg",    2015),
    ("SE01", "Sportamore-or-less AB",              "Webshop",          "Stockholm",   2016),
    ("SE01", "Subtractnature AB",                  "Webshop",          "Göteborg",    2017),
    ("SE01", "Allemansrätten AB",                  "Independent",      "Östersund",   2013),
    ("SE01", "Fika & Fjäll AB",                    "Independent",      "Åre",         2015),
    ("SE01", "Lagom Sport AB",                     "Independent",      "Uppsala",     2011),
    ("SE01", "Mysig Mountain AB",                  "Independent",      "Sälen",       2019),
    ("SE01", "Raketten Sport AB",                  "Independent",      "Malmö",       (2024, 3, 1)),  # story candidate
    ("SE01", "Online consumers (nordvidde.se)",    "Online consumers", "Göteborg",    2020),
    # Denmark
    ("DK01", "Bilkage A/S",                        "Key account",      "Aarhus",      2009),
    ("DK01", "Intersnort Danmark A/S",             "Chain store",      "Aarhus",      2007),
    ("DK01", "Sport Muster ApS",                   "Chain store",      "København",   2012),
    ("DK01", "Spejder Sjov A/S",                   "Chain store",      "Aalborg",     2011),
    ("DK01", "Abnormal A/S",                       "Chain store",      "Aarhus",      2018),
    ("DK01", "Sælling Sport A/S",                  "Chain store",      "Aarhus",      2014),
    ("DK01", "Hygge & Hiking ApS",                 "Independent",      "København",   2016),
    ("DK01", "Himmelbjerget Bjergsport ApS",       "Independent",      "Silkeborg",   2013),
    ("DK01", "Langsom & Træg ApS",                 "Independent",      "Odense",      2014),  # story candidate
    ("DK01", "Online consumers (nordvidde.dk)",    "Online consumers", "Aarhus",      2020),
    # Finland
    ("FI01", "Partiohaitta Oy",                    "Key account",      "Helsinki",    2010),
    ("FI01", "Intersnort Suomi Oy",                "Chain store",      "Helsinki",    2008),
    ("FI01", "Sockmann Oy",                        "Chain store",      "Helsinki",    2012),
    ("FI01", "Prisman't Oy",                       "Chain store",      "Tampere",     2015),
    ("FI01", "Motonot Oy",                         "Chain store",      "Tampere",     2017),
    ("FI01", "Tökmanni Oy",                        "Chain store",      "Lahti",       2018),
    ("FI01", "Verkkokauppa.con Oy",                "Webshop",          "Helsinki",    2016),
    ("FI01", "Sisu & Sauna Sport Oy",              "Independent",      "Rovaniemi",   2013),
    ("FI01", "Kalsarikännit Outdoor Oy",           "Independent",      "Tampere",     2019),
    ("FI01", "Mökki Mania Oy",                     "Independent",      "Kuopio",      2017),
    ("FI01", "Online consumers (nordvidde.fi)",    "Online consumers", "Tampere",     2021),
    # Germany
    ("DE01", "Globetrödler GmbH",                  "Key account",      "Hamburg",     2011),
    ("DE01", "SportSchreck GmbH",                  "Key account",      "München",     2013),
    ("DE01", "Decathlazy Deutschland GmbH",        "Chain store",      "Berlin",      2014),
    ("DE01", "Intersnort Deutschland GmbH",        "Chain store",      "Stuttgart",   2012),
    ("DE01", "Kaufnix GmbH",                       "Chain store",      "Köln",        2017),
    ("DE01", "Bergfeinde GmbH",                    "Webshop",          "Stuttgart",   2015),
    ("DE01", "Zalandon't SE",                      "Webshop",          "Berlin",      2016),
    ("DE01", "Wanderlust & Wurst GmbH",            "Independent",      "Garmisch-Partenkirchen", 2014),
    ("DE01", "Pünktlich Sport GmbH",               "Independent",      "Frankfurt",   2012),
    ("DE01", "Ordnung Outdoor GmbH",               "Independent",      "Hannover",    2016),
    ("DE01", "Gemütlich Gipfel GmbH",              "Independent",      "Berchtesgaden", 2018),
    ("DE01", "Online consumers (nordvidde.de)",    "Online consumers", "Hamburg",     2021),
]

# Export customers, all served by the Norwegian HQ.
# (name, segment, country_code, city, currency, since year)
EXPORT_CUSTOMERS = [
    ("Mountain Wherehouse Ltd",        "Chain store", "GB", "London",          "GBP", 2016),
    ("Go Outside-ish Ltd",             "Chain store", "GB", "Sheffield",       "GBP", 2018),
    ("Blacks & Blues Ltd",             "Chain store", "GB", "Manchester",      "GBP", 2019),
    ("Kilt & Crampons Ltd",            "Independent", "GB", "Fort William",    "GBP", 2015),
    ("Bass Amateur Shops Inc",         "Chain store", "US", "Springfield",     "USD", 2020),
    ("Frontcountry.com Inc",           "Webshop",     "US", "Salt Lake City",  "USD", 2021),
    ("Bevertje Buitensport BV",        "Chain store", "NL", "Utrecht",         "EUR", 2017),
    ("Alpenglühwein GmbH",             "Independent", "AT", "Innsbruck",       "EUR", 2019),
    ("Fondue & Firn AG",               "Independent", "CH", "Zermatt",         "EUR", 2020),
    ("Viking Vindjakki ehf",           "Independent", "IS", "Reykjavík",       "EUR", 2018),
]

# --------------------------------------------------------------------------
# Products: what can be sold, list price range in NOK, season
# --------------------------------------------------------------------------
PRODUCT_ITEMS = {
    "Apparel": [
        ("Shell Jacket", 2500, 5500, "All year"), ("Down Jacket", 2500, 6000, "Winter"),
        ("Fleece Jacket", 700, 1500, "All year"), ("Softshell Jacket", 1500, 3000, "All year"),
        ("Wool Base Layer", 500, 1200, "Winter"), ("Hiking Pants", 900, 2000, "Summer"),
        ("Wool Sweater", 1200, 2800, "Winter"), ("Technical T-shirt", 300, 600, "Summer"),
        ("Beanie", 250, 500, "Winter"), ("Gloves", 300, 900, "Winter"),
        ("Rain Jacket", 800, 2000, "Summer"), ("Shorts", 400, 900, "Summer"),
    ],
    "Footwear": [
        ("Hiking Boots", 1800, 3500, "All year"), ("Trail Running Shoes", 1200, 2200, "Summer"),
        ("Road Running Shoes", 1100, 2000, "All year"), ("Winter Boots", 1500, 3000, "Winter"),
        ("Sandals", 500, 1000, "Summer"), ("Approach Shoes", 1200, 2000, "Summer"),
    ],
    "Skis & winter": [
        ("Cross-country Skis", 1500, 5000, "Winter"), ("Alpine Skis", 3000, 8000, "Winter"),
        ("Touring Skis", 4000, 8000, "Winter"), ("Ski Boots", 2000, 5000, "Winter"),
        ("Cross-country Boots", 1200, 3000, "Winter"), ("Ski Poles", 300, 1200, "Winter"),
        ("Ski Wax", 100, 300, "Winter"), ("Ski Goggles", 600, 1800, "Winter"),
        ("Ski Helmet", 900, 2500, "Winter"), ("Snowshoes", 1200, 2500, "Winter"),
    ],
    "Tents & camping": [
        ("2-person Tent", 2500, 6000, "Summer"), ("4-person Tent", 4000, 9000, "Summer"),
        ("Sleeping Bag", 1200, 4500, "All year"), ("Sleeping Mat", 500, 1800, "Summer"),
        ("Camping Stove", 500, 1500, "Summer"), ("Cookware Set", 400, 1000, "Summer"),
        ("Headlamp", 300, 900, "All year"), ("Hammock", 400, 900, "Summer"),
        ("Camp Chair", 400, 900, "Summer"),
    ],
    "Backpacks": [
        ("Daypack", 600, 1500, "All year"), ("Trekking Backpack", 1800, 3500, "Summer"),
        ("Duffel Bag", 900, 2000, "All year"), ("Ski Backpack", 1200, 2500, "Winter"),
        ("Hydration Pack", 600, 1200, "Summer"),
    ],
    "Bikes": [
        ("Mountain Bike", 12000, 40000, "Summer"), ("Gravel Bike", 15000, 35000, "Summer"),
        ("E-bike", 25000, 50000, "Summer"), ("Bike Helmet", 700, 2000, "Summer"),
        ("Bike Lights", 300, 900, "All year"), ("Bike Lock", 300, 800, "All year"),
        ("Cycling Jersey", 600, 1400, "Summer"),
    ],
    "Climbing": [
        ("Climbing Shoes", 900, 1800, "All year"), ("Harness", 600, 1200, "All year"),
        ("Dynamic Rope", 1500, 3000, "All year"), ("Quickdraw Set", 800, 1500, "All year"),
        ("Chalk Bag", 150, 300, "All year"), ("Crash Pad", 1800, 3200, "All year"),
        ("Belay Device", 300, 700, "All year"),
    ],
    "Electronics": [
        ("GPS Watch", 2500, 7000, "All year"), ("Handheld GPS", 2500, 5000, "All year"),
        ("Power Bank", 300, 800, "All year"), ("Avalanche Transceiver", 2500, 4000, "Winter"),
        ("Action Camera", 3000, 5000, "All year"), ("Bike Computer", 1500, 4000, "Summer"),
    ],
}

# Typical gross margin on list price, per category
CATEGORY_MARGIN = {
    "Apparel": 0.50, "Footwear": 0.45, "Skis & winter": 0.38, "Tents & camping": 0.42,
    "Backpacks": 0.45, "Bikes": 0.25, "Climbing": 0.45, "Electronics": 0.20,
}
PRIVATE_LABEL_EXTRA_MARGIN = 0.12

MODEL_NAMES = [
    "Besseggen", "Trolltunga", "Galdhø", "Romsdal", "Lofoten", "Senja", "Rondane", "Jotun",
    "Hardanger", "Femund", "Lyngen", "Sunnmøre", "Dovre", "Finse", "Kebne", "Sarek",
    "Abisko", "Kungsleden", "Padjelanta", "Tärna", "Vasa", "Saana", "Koli", "Pallas",
    "Ylläs", "Nuuksio", "Inari", "Skagen", "Rold", "Mols", "Zugspitze", "Watzmann", "Harz",
    "Brocken", "Allgäu", "Svalbard", "Polar", "Nordkapp", "Vidde", "Tind", "Isbjørn", "Ulv",
    "Rein", "Elg", "Jerv", "Gaupe", "Ørn", "Ravn", "Lynx", "Aurora", "Midnatt", "Storm",
    "Kuling", "Frost", "Granitt",
]
MODEL_VARIANTS = ["", "", "", " Pro", " Lite", " GTX", " 2.0", " XT", " Light", " Expedition",
                  " Junior", " W", " M"]

# --------------------------------------------------------------------------
# Goods suppliers (handwritten)
# --------------------------------------------------------------------------
# (supplier name, brand, country, invoicing currency, what they supply, product weight)
# "What they supply" lists product categories and/or individual product types.
# Brand "Nordvidde" = our own private label, made by contract factories.
PUN_GOODS_SUPPLIERS = [
    # North America and Asia, invoicing in USD
    ("The North Farce Inc.",            "The North Farce",    "US", "USD", ["Apparel", "Tents & camping", "Backpacks"], 3),
    ("Patagucci Inc.",                  "Patagucci",          "US", "USD", ["Apparel"], 2),
    ("Arc'terrific Equipment Ltd.",     "Arc'terrific",       "CA", "USD", ["Apparel", "Climbing"], 2),
    ("Colombo Sportswear Co.",          "Colombo",            "US", "USD", ["Apparel", "Footwear"], 2),
    ("Hokus Pokus Inc.",                "Hokus Pokus",        "US", "USD", ["Trail Running Shoes", "Road Running Shoes"], 2),
    ("Babbling Brooks Inc.",            "Babbling Brooks",    "US", "USD", ["Trail Running Shoes", "Road Running Shoes"], 1),
    ("Merrily Inc.",                    "Merrily",            "US", "USD", ["Hiking Boots", "Trail Running Shoes", "Sandals"], 1),
    ("Black Rhinestone Equipment Inc.", "Black Rhinestone",   "US", "USD", ["Climbing", "Headlamp"], 1),
    ("Garmint Ltd.",                    "Garmint",            "US", "USD", ["GPS Watch", "Handheld GPS", "Bike Computer"], 2),
    ("Ostrich Packs Inc.",              "Ostrich",            "US", "USD", ["Backpacks"], 2),
    ("Basics Corporation",              "Basics",             "JP", "USD", ["Trail Running Shoes", "Road Running Shoes"], 2),
    ("Trekkie Bicycle Corp.",           "Trekkie",            "US", "USD", ["Mountain Bike", "Gravel Bike", "E-bike"], 2),
    ("Generalized Bicycles Inc.",       "Generalized",        "US", "USD", ["Mountain Bike", "Gravel Bike", "E-bike", "Bike Helmet"], 2),
    # Norway
    ("Helly Handsome AS",               "Helly Handsome",     "NO", "NOK", ["Apparel"], 3),
    ("Burgerhans of Norway AS",         "Burgerhans",         "NO", "NOK", ["Apparel", "Backpacks", "Tents & camping"], 3),
    ("Devoldemort AS",                  "Devoldemort",        "NO", "NOK", ["Wool Base Layer", "Wool Sweater", "Beanie"], 2),
    ("Dale of Nowhere AS",              "Dale of Nowhere",    "NO", "NOK", ["Wool Sweater", "Beanie", "Gloves"], 1),
    ("Ulv i Fåreklær AS",               "Ulv i Fåreklær",     "NO", "NOK", ["Wool Base Layer", "Wool Sweater", "Beanie"], 1),
    ("Swax AS",                         "Swax",               "NO", "NOK", ["Ski Wax", "Ski Poles"], 2),
    ("Madhouse Skis AS",                "Madhouse",           "NO", "NOK", ["Cross-country Skis", "Cross-country Boots", "Ski Poles"], 2),
    ("Sour Protection AS",              "Sour Protection",    "NO", "NOK", ["Ski Goggles", "Ski Helmet", "Bike Helmet"], 1),
    ("Oddlo AS",                        "Oddlo",              "NO", "NOK", ["Apparel"], 1),
    ("Kari Tråkig AS",                  "Kari Tråkig",        "NO", "NOK", ["Apparel"], 1),
    # Sweden
    ("Fjällrävioli AB",                 "Fjällrävioli",       "SE", "SEK", ["Apparel", "Backpacks"], 3),
    ("Haglöfs-Haglöfs AB",              "Haglöfs-Haglöfs",    "SE", "SEK", ["Apparel", "Footwear"], 2),
    ("Primus Inter Pares AB",           "Primus Inter Pares", "SE", "SEK", ["Camping Stove", "Cookware Set"], 1),
    ("Ultima Thule AB",                 "Ultima Thule",       "SE", "SEK", ["Daypack", "Duffel Bag", "Trekking Backpack", "Hydration Pack"], 2),
    ("Hestra-ordinary AB",              "Hestra-ordinary",    "SE", "SEK", ["Gloves", "Beanie"], 1),
    ("P.O.C. (Probably Overpriced Clothing) AB", "P.O.C.",   "SE", "SEK", ["Ski Helmet", "Ski Goggles", "Bike Helmet", "Cycling Jersey"], 1),
    ("Crafty AB",                       "Crafty",             "SE", "SEK", ["Apparel"], 1),
    ("Croissant Cyklar AB",             "Croissant",          "SE", "SEK", ["Mountain Bike", "Gravel Bike", "E-bike"], 1),
    # Rest of Europe, invoicing in EUR
    ("Salmon Outdoor SAS",              "Salmon",             "FR", "EUR", ["Footwear", "Alpine Skis", "Ski Boots", "Touring Skis"], 3),
    ("Rossignoooo SA",                  "Rossignoooo",        "FR", "EUR", ["Alpine Skis", "Ski Boots", "Cross-country Skis", "Ski Poles"], 2),
    ("Pretzl SA",                       "Pretzl",             "FR", "EUR", ["Harness", "Quickdraw Set", "Belay Device", "Headlamp"], 1),
    ("Subatomic GmbH",                  "Subatomic",          "AT", "EUR", ["Alpine Skis", "Ski Boots", "Ski Helmet", "Touring Skis"], 2),
    ("Fishy Fischer GmbH",              "Fishy Fischer",      "AT", "EUR", ["Cross-country Skis", "Cross-country Boots", "Alpine Skis"], 1),
    ("Vaudeville GmbH",                 "Vaudeville",         "DE", "EUR", ["Apparel", "Backpacks", "Tents & camping"], 2),
    ("Deuteronomy GmbH",                "Deuteronomy",        "DE", "EUR", ["Backpacks"], 2),
    ("Lowa Expectations GmbH",          "Lowa Expectations",  "DE", "EUR", ["Hiking Boots", "Approach Shoes", "Winter Boots"], 2),
    ("Jack Wolfskinny GmbH",            "Jack Wolfskinny",    "DE", "EUR", ["Apparel"], 2),
    ("Cubicle Bikes GmbH",              "Cubicle",            "DE", "EUR", ["Mountain Bike", "Gravel Bike", "E-bike"], 1),
    ("Mammutt & Mammi AG",              "Mammutt & Mammi",    "CH", "EUR", ["Climbing", "Apparel"], 2),
    ("Off Running AG",                  "Off",                "CH", "EUR", ["Trail Running Shoes", "Road Running Shoes"], 2),
    ("Scarper Srl",                     "Scarper",            "IT", "EUR", ["Climbing Shoes", "Approach Shoes", "Hiking Boots", "Ski Boots"], 1),
    ("Soonto Oy",                       "Soonto",             "FI", "EUR", ["GPS Watch", "Avalanche Transceiver"], 1),
    # Contract factories for our own private label (invented names, USD)
    ("Shenzhen Golden Peak Outdoor Co., Ltd.",       "Nordvidde", "CN", "USD", ["Apparel"], 2),
    ("Dongguan Evergreen Textile Co., Ltd.",         "Nordvidde", "CN", "USD", ["Apparel"], 2),
    ("Hangzhou Jade Valley Garments Co., Ltd.",      "Nordvidde", "CN", "USD", ["Apparel"], 2),
    ("Ningbo Bright Star Camping Co., Ltd.",         "Nordvidde", "CN", "USD", ["Tents & camping"], 2),
    ("Happy Panda Outdoor Manufacturing Co., Ltd.",  "Nordvidde", "CN", "USD", ["Tents & camping", "Backpacks"], 4),  # story candidate
    ("Ningbo Prosperous Tent Co., Ltd.",             "Nordvidde", "CN", "USD", ["2-person Tent", "4-person Tent"], 1),
    ("Guangzhou Lucky Summit Bags Co., Ltd.",        "Nordvidde", "CN", "USD", ["Backpacks"], 2),
    ("Xiamen Silver River Footwear Co., Ltd.",       "Nordvidde", "CN", "USD", ["Footwear"], 2),
    ("Saigon Harmony Apparel JSC",                   "Nordvidde", "VN", "USD", ["Apparel"], 2),
    ("Hanoi Great Mountain Garment JSC",             "Nordvidde", "VN", "USD", ["Apparel"], 2),
    ("Dong Nai Lotus Footwear Co., Ltd.",            "Nordvidde", "VN", "USD", ["Footwear"], 2),
    ("Taichung Precision Cycle Co., Ltd.",           "Nordvidde", "TW", "USD", ["Mountain Bike", "Gravel Bike", "Bike Lock"], 1),
    ("Kaohsiung Sunrise Electronics Co., Ltd.",      "Nordvidde", "TW", "USD", ["Power Bank", "Headlamp", "Bike Lights", "Bike Computer"], 2),
    ("Dhaka Northern Star Knitwear Ltd.",            "Nordvidde", "BD", "USD", ["Technical T-shirt", "Wool Base Layer", "Beanie", "Cycling Jersey"], 2),
    ("Chittagong Blue Ocean Textiles Ltd.",          "Nordvidde", "BD", "USD", ["Technical T-shirt", "Shorts", "Fleece Jacket"], 1),
]

# --------------------------------------------------------------------------
# Service suppliers (handwritten)
# --------------------------------------------------------------------------
# (name, country, invoicing currency, category, entity_id or None = used group-wide)
PUN_SERVICE_SUPPLIERS = [
    # Norway
    ("Postponed AS",                         "NO", "NOK", "Freight",            "NO01"),
    ("Bring It Maybe AS",                    "NO", "NOK", "Freight",            "NO01"),
    ("Tellnoone Norge AS",                   "NO", "NOK", "Telecom & IT",       "NO01"),
    ("Lukewarm Mobil AS",                    "NO", "NOK", "Telecom & IT",       "NO01"),
    ("Vismaybe AS",                          "NO", "NOK", "Telecom & IT",       "NO01"),
    ("Tripletax AS",                         "NO", "NOK", "Telecom & IT",       "NO01"),
    ("Elvis Strøm AS",                       "NO", "NOK", "Utilities",          "NO01"),
    ("Halvslund Strøm AS",                   "NO", "NOK", "Utilities",          "NO01"),
    ("Gjensidig Forståelse Forsikring",      "NO", "NOK", "Insurance",          "NO01"),
    ("Kinda Pricey Management Group AS",     "NO", "NOK", "Consulting & audit", "NO01"),
    ("Funn.no AS",                           "NO", "NOK", "Marketing",          "NO01"),
    ("Bank of Mum ASA",                      "NO", "NOK", "Banking",            "NO01"),
    ("Extra Eiendom AS",                     "NO", "NOK", "Rent",               "NO01"),
    ("Circle Q Norge AS",                    "NO", "NOK", "Vehicles",           "NO01"),
    ("Fjellvann Rådgivning AS",              "NO", "NOK", "Consulting & audit", "NO01"),  # story candidate
    # Sweden
    ("PostNope AB",                          "SE", "SEK", "Freight",            "SE01"),
    ("Tell-ya Sverige AB",                   "SE", "SEK", "Telecom & IT",       "SE01"),
    ("Vattenfail AB",                        "SE", "SEK", "Utilities",          "SE01"),
    ("IKKEA AB",                             "SE", "SEK", "Equipment & furniture", "SE01"),
    ("Insecuritas AB",                       "SE", "SEK", "Facility services",  "SE01"),
    ("ISSues Facility Services AB",          "SE", "SEK", "Facility services",  "SE01"),
    ("Lånsförsäkringar AB",                  "SE", "SEK", "Insurance",          "SE01"),
    ("PricewaterhouseCoolers AB",            "SE", "SEK", "Consulting & audit", "SE01"),
    ("Swedebank AB",                         "SE", "SEK", "Banking",            "SE01"),
    # Denmark
    ("TDC – Totally Disconnected A/S",       "DK", "DKK", "Telecom & IT",       "DK01"),
    ("Ørsteady Energi A/S",                  "DK", "DKK", "Utilities",          "DK01"),
    ("Utryg Forsikring A/S",                 "DK", "DKK", "Insurance",          "DK01"),
    ("Ernst & Old P/S",                      "DK", "DKK", "Consulting & audit", "DK01"),
    ("Danish Pastry Bank A/S",               "DK", "DKK", "Banking",            "DK01"),
    # Finland
    ("Misfortum Oyj",                        "FI", "EUR", "Utilities",          "FI01"),
    ("If Only Vakuutus Oy",                  "FI", "EUR", "Insurance",          "FI01"),
    ("Delightful & Touche Oy",               "FI", "EUR", "Consulting & audit", "FI01"),
    ("Nordidea Bank Abp",                    "FI", "EUR", "Banking",            "FI01"),
    ("Tampereen Toimitilat Oy",              "FI", "EUR", "Rent",               "FI01"),
    # Germany
    ("E.OFF Energie AG",                     "DE", "EUR", "Utilities",          "DE01"),
    ("Telekomisch AG",                       "DE", "EUR", "Telecom & IT",       "DE01"),
    ("Dalliance Versicherung AG",            "DE", "EUR", "Insurance",          "DE01"),
    ("DHLate Express GmbH",                  "DE", "EUR", "Freight",            "DE01"),
    ("Schenk-Me-Later GmbH",                 "DE", "EUR", "Freight",            "DE01"),
    ("Excuseture GmbH",                      "DE", "EUR", "Consulting & audit", "DE01"),
    ("Sparkassette Hamburg",                 "DE", "EUR", "Banking",            "DE01"),
    ("Hafenkante Gewerbeimmobilien GmbH",    "DE", "EUR", "Rent",               "DE01"),
    # Group-wide
    ("Mursk Line A/S",                       "DK", "USD", "Freight",            None),
    ("Microsloth Ireland Ltd",               "IE", "EUR", "Telecom & IT",       None),
    ("Salesfarce Inc.",                      "US", "USD", "Telecom & IT",       None),
    ("Amazin' Web Services EMEA SARL",       "LU", "EUR", "Telecom & IT",       None),
    ("Slacker Technologies Ltd",             "IE", "EUR", "Telecom & IT",       None),
    ("Adobo Systems Ireland Ltd",            "IE", "EUR", "Telecom & IT",       None),
    ("SAPpy AG",                             "DE", "EUR", "Telecom & IT",       None),
    ("Goggle Ireland Ltd",                   "IE", "EUR", "Marketing",          None),
    ("Meh-ta Platforms Ireland Ltd",         "IE", "EUR", "Marketing",          None),
    ("LinkedOut Ireland Ltd",                "IE", "EUR", "Marketing",          None),
    ("Indoor by ISPO GmbH",                  "DE", "EUR", "Events",             None),
    ("SASsy Airlines AB",                    "SE", "SEK", "Travel",             None),
    ("Scandalic Hotels AB",                  "SE", "SEK", "Travel",             None),
    ("Hurts Rental Europe BV",               "NL", "EUR", "Vehicles",           None),
]

# Expense account for each service category (NS 4102)
SERVICE_CATEGORY_ACCOUNT = {
    "Freight": 4060, "Rent": 6300, "Facility services": 6360, "Utilities": 6340,
    "Equipment & furniture": 6540, "Consulting & audit": 6700, "Office supplies": 6800,
    "Telecom & IT": 6900, "Vehicles": 7100, "Travel": 7140, "Marketing": 7300,
    "Events": 7320, "Insurance": 7500, "Banking": 7770,
}
# How often each category shows up among generated local suppliers
SERVICE_CATEGORY_WEIGHT = {
    "Rent": 2, "Facility services": 1.5, "Utilities": 1, "Equipment & furniture": 1,
    "Consulting & audit": 2, "Office supplies": 1, "Telecom & IT": 1.5, "Vehicles": 1.5,
    "Travel": 1.5, "Marketing": 1.5, "Events": 0.7, "Freight": 2,
}
