# -*- coding: utf-8 -*-
"""Pydantic User models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.utils import (
    JsonApiCreateBaseModel,
    JsonApiDataCreateBaseModel,
    JsonApiDataDBModel,
    JsonApiDataUpdateBaseModel,
    JsonApiDBModel,
    JsonApiUpdateBaseModel,
)


class BaseUserAttributesModel(BaseModel):
    """Base User model."""

    disabled: Optional[bool] = False
    superuser: Optional[bool] = False
    username: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    full_name: Optional[str] = None


class UserCreateAttributesModel(BaseUserAttributesModel):
    """User attributes creation serializer."""

    ext_id: str
    username: str


class UserCreateModel(JsonApiCreateBaseModel):
    """User creation serializer."""

    type: str = "user"  # noqa: A003, VNE003
    attributes: UserCreateAttributesModel


class UserDataCreateModel(JsonApiDataCreateBaseModel):
    """User data creation serializer."""

    data: UserCreateModel


class UserUpdateModel(BaseUserAttributesModel):
    """User attributes update serializer."""


class UserUpdateModel(JsonApiUpdateBaseModel):
    """User update serializer."""

    type: str = "user"  # noqa: A003, VNE003
    attributes: UserUpdateModel


class UserDataUpdateModel(JsonApiDataUpdateBaseModel):
    """User data update serializer."""

    data: UserUpdateModel


class BaseUserDB(BaseModel):
    """User database row attributes model."""

    ext_id: str
    disabled: bool
    superuser: bool
    created: datetime
    username: str
    given_name: Optional[str]
    family_name: Optional[str]
    full_name: Optional[str]


class UserDBModel(JsonApiDBModel):
    """User serializer."""

    attributes: BaseUserDB


class UserDBDataModel(JsonApiDataDBModel):
    """User data model."""

    data: UserDBModel

    @property
    def disabled(self):
        """Interface for UserGinoModel.disabled."""
        return self.data.attributes.disabled
