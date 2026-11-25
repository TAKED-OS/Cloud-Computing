"""Process capsule.sealed messages delivered directly by SNS to SQS."""
import json
import logging
import os
import time

import psycopg

LOGGER = logging.getLogger(__name__)
SQL = """
WITH event AS (
    INSERT INTO notification_events (event_id)
    VALUES (%s) ON CONFLICT DO NOTHING
    RETURNING event_id
)
INSERT INTO notifications (capsule_id, user_id, recipient, message)
SELECT c.id, c.user_id, COALESCE(c.recipient_email, u.email),
       concat('Capsule "', c.title, '" was sealed.')
FROM event
JOIN capsules c ON c.id = %s
JOIN users u ON u.id = c.user_id
"""


def handle(event, _context):
    failures = []
    for record in event["Records"]:
        try:
            message = json.loads(record["body"])
            capsule_id = message["capsule_id"]
            if (
                message["type"] != "capsule.sealed"
                or message["version"] != 1
                or type(capsule_id) is not int
                or capsule_id < 1
                or message["event_id"] != f"capsule.sealed:{capsule_id}"
            ):
                raise ValueError("Invalid capsule.sealed event")
            with psycopg.connect(
                os.environ["DATABASE_URL"], sslmode="require", connect_timeout=5
            ) as connection:
                # A missing record must leave the event eligible for retry.
                row = connection.execute(
                    "SELECT id FROM capsules WHERE id = %s FOR KEY SHARE", (capsule_id,)
                ).fetchone()
                if row is None:
                    raise ValueError("Capsule does not exist")
                time.sleep(float(os.environ.get("MAIL_DELAY_SECONDS", "3")))
                connection.execute(SQL, (message["event_id"], capsule_id))
        except (psycopg.Error, KeyError, TypeError, ValueError):
            LOGGER.warning("Failed to process SQS message %s", record["messageId"])
            failures.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": failures}
