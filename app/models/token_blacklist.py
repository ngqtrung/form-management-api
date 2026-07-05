from app.extensions import db
from app.models.base import BaseModel


class TokenBlacklist(BaseModel):
    __tablename__ = "token_blacklist"

    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.TIMESTAMP(timezone=False), nullable=False, index=True)
