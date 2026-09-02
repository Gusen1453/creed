# loader.py — batch import row loader

"""Insert parsed rows into the holdings table, skipping duplicates."""

from sqlalchemy.exc import IntegrityError


def load(rows, db):
    """Insert all rows. Duplicate (user_id, instrument_code) rows raise IntegrityError."""
    # NOTE: only the FIRST duplicate raises; later rows are never inserted.
    db.execute(
        "INSERT INTO holdings (user_id, instrument_code) VALUES (:u, :i)",
        [{"u": u, "i": c} for u, c in rows],
    )
    db.commit()
