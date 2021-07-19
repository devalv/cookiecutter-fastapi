# -*- coding: utf-8 -*-
"""ORM Models for Auth entities."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.config import (
    ACCESS_TOKEN_EXPIRE_MIN,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from core.utils import CREDENTIALS_EX, JsonApiGinoModel

from .. import db

ref_token_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(db.Model, JsonApiGinoModel):
    """Yep, this is a User table."""

    __tablename__ = "user"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A002, A003, VNE003
    ext_id = db.Column(db.Unicode(length=255), nullable=False, unique=True)
    disabled = db.Column(db.Boolean(), nullable=False, default=False)
    superuser = db.Column(db.Boolean(), nullable=False, default=False)
    created = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    username = db.Column(db.Unicode(length=255), nullable=False, index=True)
    given_name = db.Column(db.Unicode(length=255), nullable=True)
    family_name = db.Column(db.Unicode(length=255), nullable=True)
    full_name = db.Column(db.Unicode(length=255), nullable=True)

    @property
    def id_str(self):
        """Str representation for a self.id."""
        return str(self.id)

    @property
    def active(self):
        return not self.disabled

    def create_access_token(self):
        """Create for a user new access token."""
        token_data = {
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN),
            "id": self.id_str,
            "username": self.username,
        }
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    async def create_refresh_token(self):
        """Create for a user new refresh token."""
        token_data = {
            "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "id": self.id_str,
            "username": self.username,
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        await TokenInfo.add_token(user_id=self.id, refresh_token=token)
        return token

    async def delete_refresh_token(self):
        """Delete for a user existing refresh token."""
        return await TokenInfo.delete.where(TokenInfo.user_id == self.id).gino.status()

    async def create_token(self):
        acc_token = self.create_access_token()
        ref_token = await self.create_refresh_token()
        return {
            "access_token": acc_token,
            "refresh_token": ref_token,
            "token_type": "bearer",
            "alg": ALGORITHM,
            "typ": "JWT",
        }

    async def token_info(self):
        """Get user existing token information."""
        return await TokenInfo.get(self.id)

    async def token_is_valid(self, token: str) -> bool:
        """Checking that the token matches the issued one."""
        token_info = await self.token_info()
        return token_info and token_info.verify_token(token)

    @classmethod
    async def insert_or_update_by_ext_id(
        cls,
        sub: str,
        username: str,
        family_name: str = None,
        given_name: str = None,
        full_name: str = None,
        **__
    ) -> User:
        """Create new record or update existing."""

        user_obj = await cls.query.where(cls.ext_id == sub).gino.first()
        if user_obj and user_obj.active:
            await user_obj.update(
                username=username,
                family_name=family_name,
                given_name=given_name,
                full_name=full_name,
            ).apply()
        elif not user_obj:
            user_obj = await cls.create(
                ext_id=sub,
                username=username,
                family_name=family_name,
                given_name=given_name,
                full_name=full_name,
            )
        else:
            raise CREDENTIALS_EX
        return user_obj


class TokenInfo(db.Model):
    """Token information, such as user to whom token was claimed."""

    __tablename__ = "token_info"

    user_id = db.Column(
        UUID(), db.ForeignKey(User.id, ondelete="CASCADE"), primary_key=True
    )
    refresh_token = db.Column(db.Unicode(), nullable=False, index=True)
    created = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    @staticmethod
    def get_refresh_token_hash(token: str):
        """Hash plain token str."""
        return ref_token_context.hash(token)

    @classmethod
    async def add_token(cls, user_id: UUID, refresh_token: str):
        """Add new refresh_token for a user."""
        async with db.transaction():
            await cls.delete.where(cls.user_id == user_id).gino.status()
            await cls.create(
                user_id=user_id, refresh_token=cls.get_refresh_token_hash(refresh_token)
            )

    def verify_token(self, refresh_token: str):
        """Verify plain token text and stored hashed value."""
        return ref_token_context.verify(refresh_token, self.refresh_token)
