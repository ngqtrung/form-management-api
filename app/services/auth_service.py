import jwt

from app.auth.jwt_utils import decode_token, encode_access_token, encode_refresh_token
from app.errors import AuthenticationError
from app.extensions import db
from app.models.token_blacklist import TokenBlacklist
from app.models.user import User


class AuthService:
    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user is None or user.status != "active" or not user.check_password(password):
            raise AuthenticationError("Invalid email or password.")

        access_token, _ = encode_access_token(user)
        refresh_token, _ = encode_refresh_token(user)
        return {"access_token": access_token, "refresh_token": refresh_token, "user": user.to_json()}

    def refresh(self, refresh_token):
        try:
            payload = decode_token(refresh_token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Refresh token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid refresh token.")

        if payload.get("type") != "refresh":
            raise AuthenticationError("Expected a refresh token.")

        if TokenBlacklist.query.filter_by(jti=payload.get("jti")).first() is not None:
            raise AuthenticationError("Refresh token has been revoked.")

        user = db.session.get(User, payload.get("sub"))
        if user is None or user.status != "active":
            raise AuthenticationError("User not found or inactive.")

        access_token, _ = encode_access_token(user)
        return {"access_token": access_token}

    def logout(self, jti, expires_at):
        db.session.add(TokenBlacklist(jti=jti, expires_at=expires_at))
        db.session.commit()
