# -*- coding: utf-8 -*-
"""Project API by versions."""

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_versioning import VersionedFastAPI

from core.config import SWAP_TOKEN_ENDPOINT
from core.database import db

from .v1 import security_router  # noqa: I201


def get_app() -> FastAPI:
    """Just simple application initialization."""
    return FastAPI(
        title="{{ cookiecutter.project_short_description }}",
        version="0.1.0",
        swagger_ui_oauth2_redirect_url=SWAP_TOKEN_ENDPOINT,
        swagger_ui_init_oauth={
            "clientId": "please keep this value",
            "clientSecret": "please keep this value",
            "appName": "{{ cookiecutter.project_name }}",
        },
    )


def configure_routes(application: FastAPI):
    """Configure application."""
    application.include_router(security_router)
    add_pagination(application)


def get_versioned_app(application: FastAPI) -> VersionedFastAPI:
    return VersionedFastAPI(
        application,
        version_format="{major}",
        prefix_format="/api/v{major}",
        swagger_ui_oauth2_redirect_url=SWAP_TOKEN_ENDPOINT,
    )


def configure_db(application: FastAPI):
    db.init_app(application)


app = get_app()
configure_routes(application=app)
app = get_versioned_app(application=app)
configure_db(app)


__all__ = ["app", "db"]
