# -*- coding: utf-8 -*-
"""Project extra utils."""

from .exceptions import (
    CREDENTIALS_EX,
    INACTIVE_EX,
    NOT_AN_OWNER,
    NOT_IMPLEMENTED_EX,
    OAUTH2_EX,
)
from .fastapi_pagination import JsonApiPage
from .gino_models import JsonApiGinoModel
from .pydantic_models import (
    JsonApiCreateBaseModel,
    JsonApiDataCreateBaseModel,
    JsonApiDataDBModel,
    JsonApiDataUpdateBaseModel,
    JsonApiDBModel,
    JsonApiUpdateBaseModel,
)

__all__ = [
    "JsonApiPage",
    "JsonApiGinoModel",
    "JsonApiDBModel",
    "JsonApiDataCreateBaseModel",
    "JsonApiDataUpdateBaseModel",
    "JsonApiDataDBModel",
    "JsonApiCreateBaseModel",
    "JsonApiUpdateBaseModel",
    "CREDENTIALS_EX",
    "INACTIVE_EX",
    "OAUTH2_EX",
    "NOT_IMPLEMENTED_EX",
    "NOT_AN_OWNER",
]
