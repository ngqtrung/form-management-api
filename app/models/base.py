import uuid
from datetime import datetime, timezone

from app.extensions import db


def utcnow():
    # Deliberately naive (tzinfo stripped): stored/read consistently as UTC on both
    # PostgreSQL (TIMESTAMP WITHOUT TIME ZONE) and SQLite (used by the test suite),
    # avoiding SQLite's inability to round-trip timezone-aware datetime strings.
    return datetime.now(timezone.utc).replace(tzinfo=None)


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.TIMESTAMP(timezone=False), default=utcnow, nullable=False, index=True)
    updated_at = db.Column(
        db.TIMESTAMP(timezone=False), default=utcnow, onupdate=utcnow, nullable=False, index=True
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def to_json(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
