# -*- coding: utf-8 -*-
"""Pydantic oauth2 models."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from jose import jwt
from pydantic import UUID4, BaseModel, EmailStr, SecretStr, conint, constr, validator

from core.config import ALGORITHM, GOOGLE_CLIENT_ID, SECRET_KEY


class RefreshToken(BaseModel):
    id: UUID4  # noqa: A003, VNE003
    username: str
    exp: conint(gt=datetime.utcnow().timestamp())

    @classmethod
    def decode(cls, token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    @classmethod
    def decode_and_create(cls, token: str):
        decoded_token = cls.decode(token)
        return cls(**decoded_token)


class AccessToken(RefreshToken):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    alg: str
    typ: str

    @validator("typ")
    def typ_check(cls, value):
        assert value == "JWT"
        return value

    @validator("alg")
    def alg_check(cls, value):
        assert value == ALGORITHM
        return value

    @validator("token_type")
    def token_type_check(cls, value):
        assert value.lower() == "bearer"
        return value


class GoogleIdInfo(BaseModel):
    """Google ID token's payload.

    Attributes:
        aud: The audience that this ID token is intended for.
        exp: Expiration time which the ID token must not be accepted.
        iat: The time the ID token was issued.
        iss: The Issuer Identifier for the Issuer of the response.
        sub: An unique identifier for the user.
        at_hash: Access token hash.
        name: The user's full name, in a displayable form.
        given_name: The user's given name(s) or first name(s).
        family_name: The user's surname(s) or last name(s).
        picture: The URL of the user's profile picture.
        locale: The user's locale.

    https://developers.google.com/identity/protocols/oauth2/openid-connect#obtainuserinfo
    """

    aud: SecretStr
    exp: conint(gt=datetime.utcnow().timestamp())
    iat: datetime
    iss: constr(
        regex=r"^(https://accounts\.google\.com|accounts\.google\.com)$"  # noqa: F722
    )
    sub: str
    at_hash: Optional[str]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    email: Optional[EmailStr]

    @validator("aud")
    def aud_must_equals_gci(cls, value):
        assert value._secret_value == GOOGLE_CLIENT_ID
        return value

    @property
    def username(self):
        """Generate unique username."""
        if self.email:
            username = self.email.split("@")[0]
        elif self.name:
            username = f"{self.name}-{str(uuid4())[:8]}"
        else:
            username = f"user-{str(uuid4())[:8]}"
        return username
