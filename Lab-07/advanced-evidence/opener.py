"""Open due capsules and record in-app notices in one PostgreSQL transaction."""
import os

import psycopg

SQL = """
WITH opened AS (
    UPDATE capsules
    SET opened_at = (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
    WHERE opened_at IS NULL AND open_at <= (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
    RETURNING id, user_id, title, recipient_email
)
INSERT INTO notifications (capsule_id, user_id, recipient, message)
SELECT opened.id, opened.user_id, COALESCE(opened.recipient_email, users.email),
       concat('Capsule "', opened.title, '" is open.')
FROM opened JOIN users ON users.id = opened.user_id
RETURNING capsule_id
"""


def handle(_event, _context):
    with psycopg.connect(
        os.environ["DATABASE_URL"], sslmode="require", connect_timeout=5
    ) as connection:
        capsule_ids = [row[0] for row in connection.execute(SQL)]
    return {"opened": capsule_ids}
