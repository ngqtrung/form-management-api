import jwt
from flask import request

from app.auth.jwt_utils import decode_token
from app.errors import AuthenticationError
from app.extensions import db
from app.models.token_blacklist import TokenBlacklist
from app.models.user import User


def load_current_user():
    """Resolve the current user from the request's JWT.

    Permissions are always resolved fresh from the database (via the user's
    current roles) rather than trusting the JWT payload, so a role/permission
    change takes effect immediately without waiting for token expiry.
    """
    payload = decode_bearer_token(required_type="access")

    user = db.session.get(User, payload.get("sub"))
    if user is None or user.status != "active":
        raise AuthenticationError("User not found or inactive.")

    return user


def decode_bearer_token(required_type):
    """Decode the request's Bearer token, enforcing its `type` claim and
    rejecting it if its `jti` has been blacklisted (logged out).
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise AuthenticationError("Missing or malformed Authorization header.")

    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired.")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token.")

    if payload.get("type") != required_type:
        raise AuthenticationError(f"Expected a {required_type} token.")

    if TokenBlacklist.query.filter_by(jti=payload.get("jti")).first() is not None:
        raise AuthenticationError("Token has been revoked.")

    return payload
