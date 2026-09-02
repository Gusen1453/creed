# parser.py — batch import CSV parser

"""Parse an uploaded CSV into rows of (user_id, instrument_code)."""

import csv


def parse(text):
    """Return the list of rows. Assume each row is exactly [user_id, instrument_code]."""
    rows = []
    for line in csv.reader(text.splitlines()):
        if not line:
            continue
        user_id = line[0]
        instrument_code = line[1]
        rows.append((user_id, instrument_code))
    return rows
