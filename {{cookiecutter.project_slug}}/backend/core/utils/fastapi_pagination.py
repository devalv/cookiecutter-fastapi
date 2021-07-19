# -*- coding: utf-8 -*-
"""Fastapi-pagination extra utils."""
from __future__ import annotations

from typing import Generic, Sequence, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractParams
from fastapi_pagination.links import Page

T = TypeVar("T")


class JsonApiPage(Page[T], Generic[T]):
    """JSON:API 1.0 specification says that result key should be a `data`."""

    data: Sequence[T]

    @classmethod
    def create(
        cls, items: Sequence[T], total: int, params: AbstractParams
    ) -> JsonApiPage[T]:
        """Same as the original Page.create instead of `data`."""
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(total=total, data=items, page=params.page, size=params.size)

    class Config:  # noqa: D106
        fields = {"items": {"alias": "data"}}
