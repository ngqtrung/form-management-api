import uuid
from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app


def _encode(user, token_type, expires_delta):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user.id,
        "jti": str(uuid.uuid4()),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    if token_type == "access":
        payload["email"] = user.email
        payload["roles"] = user.role_names()

    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token, payload


def encode_access_token(user):
    return _encode(user, "access", timedelta(minutes=current_app.config["JWT_EXPIRES_MINUTES"]))


def encode_refresh_token(user):
    return _encode(user, "refresh", timedelta(days=current_app.config["REFRESH_TOKEN_EXPIRES_DAYS"]))


def decode_token(token):
    return jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
