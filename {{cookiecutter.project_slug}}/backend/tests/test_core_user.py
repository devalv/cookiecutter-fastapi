# -*- coding: utf-8 -*-
"""User core tests."""
import os
from datetime import datetime

import pytest
from asyncpg.pgproto.pgproto import UUID as UUID_PG

from core.database import TokenInfoGinoModel, UserGinoModel
from core.schemas import (
    UserDataCreateModel,
    UserDataUpdateModel,
    UserDBDataModel,
    UserDBModel,
)

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.auth,
    pytest.mark.security,
]


@pytest.fixture
async def user_shortened_mock():
    return {"ext_id": "2" * 100, "username": "user_mock"}


@pytest.fixture
async def user_shortened_ser_mock(user_shortened_mock):
    return {"data": {"attributes": user_shortened_mock}}


@pytest.fixture
async def user_extra_ser_mock(user_admin_mock):
    return {"data": {"attributes": user_admin_mock}}


class TestUserDB:
    """User db-table tests."""

    @pytest.mark.api_base
    async def test_user_default_create(self, backend_app, user_mock):
        user_obj = await UserGinoModel.create(**user_mock)
        assert user_obj.ext_id == user_mock["ext_id"]
        assert user_obj.disabled == user_mock["disabled"]
        assert user_obj.superuser == user_mock["superuser"]
        assert user_obj.username == user_mock["username"]
        assert user_obj.given_name == user_mock["given_name"]
        assert user_obj.full_name == user_mock["full_name"]
        assert user_obj.family_name == user_mock["family_name"]
        assert isinstance(user_obj.created, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_shortened_create(self, backend_app, user_shortened_mock):
        user_obj = await UserGinoModel.create(**user_shortened_mock)
        assert user_obj.ext_id == user_shortened_mock["ext_id"]
        assert user_obj.disabled is False
        assert user_obj.superuser is False
        assert user_obj.username == user_shortened_mock["username"]
        assert user_obj.given_name is None
        assert user_obj.full_name is None
        assert user_obj.family_name is None
        assert isinstance(user_obj.created, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_extra_create(self, backend_app, user_admin_mock):
        user_obj = await UserGinoModel.create(**user_admin_mock)
        assert user_obj.ext_id == user_admin_mock["ext_id"]
        assert user_obj.disabled == user_admin_mock["disabled"]
        assert user_obj.superuser == user_admin_mock["superuser"]
        assert user_obj.username == user_admin_mock["username"]
        assert user_obj.given_name == user_admin_mock["given_name"]
        assert user_obj.full_name == user_admin_mock["full_name"]
        assert user_obj.family_name == user_admin_mock["family_name"]
        assert isinstance(user_obj.created, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_get(self, backend_app, single_admin):
        assert isinstance(single_admin.data["id"], UUID_PG)
        assert single_admin.data["id"] == single_admin.id
        assert single_admin.data["type"] == "user"
        attributes = single_admin.data["attributes"]
        assert isinstance(attributes["created"], datetime)
        assert attributes["created"] == single_admin.created
        assert attributes["ext_id"] == single_admin.ext_id
        assert attributes["family_name"] == single_admin.family_name
        assert attributes["full_name"] == single_admin.full_name
        assert attributes["given_name"] == single_admin.given_name
        assert attributes["superuser"] == single_admin.superuser
        assert attributes["username"] == single_admin.username
        assert "type" not in attributes


class TestUserPydantic:
    """User pydantic serializer tests."""

    @pytest.mark.api_base
    async def test_user_serializer_get(self, backend_app, single_admin):
        serializer = UserDBDataModel.from_orm(single_admin)
        assert isinstance(serializer, UserDBDataModel)
        assert isinstance(serializer.data, UserDBModel)
        assert serializer.data.id == single_admin.id
        assert serializer.data.type == single_admin.type
        assert serializer.data.attributes.ext_id == single_admin.ext_id
        assert serializer.data.attributes.disabled == single_admin.disabled
        assert serializer.disabled == single_admin.disabled
        assert serializer.data.attributes.superuser == single_admin.superuser
        assert serializer.data.attributes.created == single_admin.created
        assert serializer.data.attributes.username == single_admin.username
        assert serializer.data.attributes.given_name == single_admin.given_name
        assert serializer.data.attributes.family_name == single_admin.family_name
        assert serializer.data.attributes.full_name == single_admin.full_name

    @pytest.mark.api_base
    async def test_user_serializer_short_create(
        self, backend_app, user_shortened_ser_mock
    ):
        serializer = UserDataCreateModel.parse_obj(user_shortened_ser_mock)
        assert isinstance(serializer, UserDataCreateModel)
        assert serializer.data.type == "user"
        assert (
            serializer.data.attributes.ext_id
            == user_shortened_ser_mock["data"]["attributes"]["ext_id"]  # noqa: W503
        )
        assert (
            serializer.data.attributes.username
            == user_shortened_ser_mock["data"]["attributes"]["username"]  # noqa: W503
        )
        db_obj = await UserGinoModel.create(**serializer.data.validated_attributes)
        assert db_obj.ext_id == serializer.data.attributes.ext_id
        assert db_obj.disabled is False
        assert db_obj.superuser is False
        assert db_obj.username == serializer.data.attributes.username
        assert db_obj.given_name is None
        assert db_obj.full_name is None
        assert db_obj.family_name is None
        assert isinstance(db_obj.created, datetime)
        assert isinstance(db_obj.id, UUID_PG)
        await db_obj.delete()

    @pytest.mark.api_base
    async def test_user_serializer_extra_create(self, backend_app, user_extra_ser_mock):
        serializer = UserDataCreateModel.parse_obj(user_extra_ser_mock)
        assert isinstance(serializer, UserDataCreateModel)
        db_obj = await UserGinoModel.create(**serializer.data.validated_attributes)
        assert db_obj.ext_id == serializer.data.attributes.ext_id
        assert db_obj.disabled == serializer.data.attributes.disabled
        assert db_obj.superuser == serializer.data.attributes.superuser
        assert db_obj.username == serializer.data.attributes.username
        assert db_obj.given_name == serializer.data.attributes.given_name
        assert db_obj.full_name == serializer.data.attributes.full_name
        assert db_obj.family_name == serializer.data.attributes.family_name
        assert isinstance(db_obj.created, datetime)
        assert isinstance(db_obj.id, UUID_PG)
        await db_obj.delete()

    @pytest.mark.api_base
    async def test_user_serializer_update(
        self, backend_app, single_admin, user_shortened_ser_mock
    ):
        serializer = UserDataUpdateModel.parse_obj(user_shortened_ser_mock)
        assert isinstance(serializer, UserDataUpdateModel)
        assert serializer.data.type == "user"
        await single_admin.update(**serializer.data.validated_attributes).apply()
        assert single_admin.disabled is False
        assert single_admin.superuser is False


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
class TestUserToken:
    """User token tests."""

    async def test_create_access_token(self, backend_app, single_admin):
        access_token = single_admin.create_access_token()
        assert isinstance(access_token, str)

    async def test_create_refresh_token(self, backend_app, single_admin):
        refresh_token = await single_admin.create_refresh_token()
        assert isinstance(refresh_token, str)

    async def test_delete_refresh_token(self, backend_app, single_admin):
        await single_admin.create_token()
        token_obj = await TokenInfoGinoModel.get(single_admin.id)
        assert token_obj
        await single_admin.delete_refresh_token()
        token_obj = await TokenInfoGinoModel.get(single_admin.id)
        assert not token_obj

    async def test_create_token(self, backend_app, single_admin):
        token = await single_admin.create_token()
        assert isinstance(token, dict)

    async def test_token_info(self, backend_app, single_admin):
        await single_admin.create_token()
        token_info = await single_admin.token_info()
        assert isinstance(token_info, TokenInfoGinoModel)

    async def test_token_is_valid(self, backend_app, single_admin):
        token_is_valid = await single_admin.token_is_valid("bad")
        assert not token_is_valid

    async def test_update_by_ext_id(self, backend_app, single_admin):
        updated_user = await single_admin.insert_or_update_by_ext_id(
            sub="1", username="updated"
        )
        assert single_admin.username != updated_user.username

    async def test_create_by_ext_id(self, backend_app):
        created_user = await UserGinoModel.insert_or_update_by_ext_id(
            sub="1", username="new-user"
        )
        assert isinstance(created_user, UserGinoModel)
