"""
Planted stories for the Nordvidde Group dataset.

Each story returns ledger events. The ledger generator (step 5) weaves them in
with the ordinary transactions, gives them journal IDs in date order (so the
IDs don't give them away) and records each one in the answer key.

Event: dict(entity_id, posting_date, created_at, source, document_no,
            description, user_id, approved_by, lines, issue)
  lines: [(account_id, currency_code, amount_currency, amount)], amount in the
         entity's functional currency, debit positive, sums to zero
  issue: (issue_type, description) for the answer key
"""
import random
from datetime import date, datetime, time, timedelta

from config import START_DATE, END_DATE, SEED, APPROX_FX_TO_NOK
from name_lists import ROGER_TRIPS

# Stories are generated up to this date and then cut at END_DATE, so the
# random draws (and the events) don't depend on the month the script runs.
STORY_HORIZON = date(2030, 12, 31)

SEASON_MONTHS = {"Winter": {12, 1, 2, 3, 4}, "Summer": {5, 6, 7, 8, 9}, "Any": set(range(1, 13))}


def fx_lookup(con):
    """{(date, currency): NOK per unit} from fx_rates."""
    return {(d, c): float(r) for d, c, r in
            con.execute("SELECT rate_date, currency_code, rate_to_nok FROM fx_rates").fetchall()}


def months(start, end):
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def weekend_days(y, m):
    d = date(y, m, 1)
    days = []
    while d.month == m:
        if d.isoweekday() >= 6:
            days.append(d)
        d += timedelta(days=1)
    return days


# --------------------------------------------------------------------------
# Roger's private weekend trips
# --------------------------------------------------------------------------
# Per year: (weights for 0, 1, 2, 3 trips a month, price multiplier,
# share of cheap trips). Starts small and careful, gets bolder every year.
ROGER_TRIP_PHASES = {
    2023: ([2, 1, 0, 0], 0.8, 1.0),   # only trips under 5,000 NOK
    2024: ([1, 9, 0, 0], 1.0, 0.6),
    2025: ([0, 0, 2, 1], 1.2, 0.3),
    2026: ([0, 0, 1, 2], 1.5, 0.2),   # and later years
}
CHEAP_TRIP_NOK = 5_000   # trips whose top price is below this count as cheap


def roger_trips(con):
    """Roger (rogerb) books private weekend trips at NO01 as travel expenses
    (7140), paid straight from the bank (1920) to himself. Manual journals,
    posted on Saturday/Sunday evenings, approved by himself."""
    rng = random.Random(f"{SEED}-roger-trips")
    fx = fx_lookup(con)
    events = []
    for y, m in months(START_DATE, STORY_HORIZON):
        weights, multiplier, cheap_share = ROGER_TRIP_PHASES[min(y, max(ROGER_TRIP_PHASES))]
        n = rng.choices(range(4), weights=weights)[0]
        in_season = [t for t in ROGER_TRIPS if m in SEASON_MONTHS[t[2]]]
        cheap = [t for t in in_season if t[4] < CHEAP_TRIP_NOK]
        for day in sorted(rng.sample(weekend_days(y, m), n)):
            pool = cheap if rng.random() < cheap_share else in_season
            description, currency, _, lo, hi = rng.choice(pool)
            nok = rng.uniform(lo, hi) * multiplier
            amount_currency = round(nok / APPROX_FX_TO_NOK[currency], 2)
            evening = time(rng.randint(19, 23), rng.randint(0, 59), rng.randint(0, 59))
            if not START_DATE <= day <= END_DATE:
                continue
            amount = round(amount_currency * fx[(day, currency)], 2)
            events.append(dict(
                entity_id="NO01", posting_date=day, created_at=datetime.combine(day, evening),
                source="MANUAL", document_no=None, description=description,
                user_id="rogerb", approved_by="rogerb",
                lines=[(7140, currency, amount_currency, amount),
                       (1920, "NOK", -amount, -amount)],
                issue=("Personal expense booked as travel",
                       f"rogerb booked a private trip as travel expense and approved it himself: "
                       f"'{description}', {amount:,.2f} NOK"),
            ))
    return events
