# -*- coding: utf-8 -*-
"""Pydantic models extra utils.

The main idea is to have a standard format for model interfaces.
"""

from abc import abstractmethod

from pydantic import UUID4, BaseModel


class JsonApiAttributesBaseModel(BaseModel):
    """Abstract attributes pydantic model."""

    @abstractmethod
    def __init__(self):
        """Main model should be redefined."""


class JsonApiCreateBaseModel(BaseModel):
    """Pydantic BaseModel extra utilities."""

    type: str  # noqa: A002, A003, VNE003
    attributes: JsonApiAttributesBaseModel

    @property
    def validated_attributes(self):
        """Validated model attributes."""
        result = dict()

        for attr, attr_value in self.attributes:
            result[attr] = attr_value

        return result

    @property
    def non_null_attributes(self):
        """Return non-null only attributes values."""
        result = dict()

        for attr, attr_value in self.attributes:
            if attr_value is not None:
                result[attr] = attr_value

        return result


class JsonApiDataCreateBaseModel(BaseModel):
    """Pydantic JSON:API data creation model."""

    data: JsonApiCreateBaseModel


class JsonApiUpdateBaseModel(JsonApiCreateBaseModel):
    """Pydantic update model."""


class JsonApiDataUpdateBaseModel(JsonApiDataCreateBaseModel):
    """Pydantic JSON:API data update model."""


class JsonApiDBModel(JsonApiCreateBaseModel):
    """Pydantic object model.

    It`s a proper response_model for JsonApiPage,
    for other response_models use JsonApiDataDBModel instead.
    """

    id: UUID4  # noqa: A002, A003, VNE003

    class Config:  # noqa: D106
        orm_mode = True


class JsonApiDataDBModel(BaseModel):
    """JSON:API says that `data` key must be on a response."""

    data: JsonApiDBModel

    class Config:  # noqa: D106
        orm_mode = True
