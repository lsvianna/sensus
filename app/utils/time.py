from datetime import datetime, timezone


def utcnow():
    """Return a naive UTC datetime for the existing database columns."""

    return datetime.now(timezone.utc).replace(tzinfo=None)
