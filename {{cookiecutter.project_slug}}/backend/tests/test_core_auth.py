# -*- coding: utf-8 -*-
"""Core auth tests."""
import os
from datetime import datetime, timedelta
from random import randint

import pytest
from fastapi import HTTPException, status
from jose import jwt
from pydantic import ValidationError

from core.config import ACCESS_TOKEN_EXPIRE_MIN, ALGORITHM, GOOGLE_CLIENT_ID
from core.database import TokenInfoGinoModel, UserGinoModel
from core.schemas import GoogleIdInfo
from core.services.security import (
    get_current_user,
    get_or_create_user,
    get_user_for_refresh,
)
from core.utils.exceptions import CREDENTIALS_EX, INACTIVE_EX

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.auth,
    pytest.mark.security,
]


API_URL_PREFIX = "/api/v1"


@pytest.fixture
async def google_id_info():
    token_info = dict()
    token_info["aud"] = GOOGLE_CLIENT_ID
    token_info["exp"] = (datetime.utcnow() + timedelta(days=1)).timestamp()
    token_info["iat"] = datetime.utcnow().timestamp()
    token_info["iss"] = "accounts.google.com"
    token_info["sub"] = str(randint(1, 999)) * 84
    token_info["given_name"] = "larry"
    token_info["family_name"] = "brin"
    return GoogleIdInfo(**token_info)


@pytest.fixture
async def existing_user_id_info(google_id_info, single_admin):
    google_id_info.sub = single_admin.ext_id
    return google_id_info


@pytest.fixture
async def existing_deactivated_user_id_info(google_id_info, single_disabled_user):
    google_id_info.sub = single_disabled_user.ext_id
    return google_id_info


@pytest.fixture
async def token_data(single_admin) -> dict:
    return {
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN),
        "id": single_admin.id_str,
        "username": single_admin.username,
    }


@pytest.fixture
async def bad_token(token_data) -> dict:

    return {
        "access_token": jwt.encode(token_data, "qwe", algorithm=ALGORITHM),
        "refresh_token": jwt.encode(token_data, "qwe", algorithm=ALGORITHM),
        "token_type": "bearer",
        "alg": ALGORITHM,
        "typ": "JWT",
    }


@pytest.fixture
async def bad_access_token(bad_token) -> str:
    return bad_token["access_token"]


@pytest.fixture
async def no_refresh_token(single_admin):
    token = await TokenInfoGinoModel.get(single_admin.id)
    await token.delete()


@pytest.fixture
async def single_admin_refresh_token(single_admin_token) -> str:
    return single_admin_token["refresh_token"]


@pytest.fixture
async def single_disabled_admin_token(single_admin_access_token, single_admin) -> str:
    await single_admin.update(disabled=True).apply()
    return single_admin_access_token


@pytest.fixture
async def single_disabled_refresh_token(
    single_admin_refresh_token, single_admin
) -> str:
    await single_admin.update(disabled=True).apply()
    return single_admin_refresh_token


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
class TestGoogleIdInfoPydantic:
    """Pydantic model tests."""

    def test_with_email(self):
        serializer = GoogleIdInfo(
            email="jeff@mail.ru",
            aud=GOOGLE_CLIENT_ID,
            sub="1",
            iat=datetime.utcnow().timestamp(),
            exp=(datetime.utcnow() + timedelta(days=1)).timestamp(),
            iss="accounts.google.com",
        )
        assert isinstance(serializer, GoogleIdInfo)
        assert serializer.username == "jeff"

    def test_aud(self):
        try:
            GoogleIdInfo(
                aud=123,
                sub="1",
                iat=datetime.utcnow().timestamp(),
                exp=(datetime.utcnow() + timedelta(days=1)).timestamp(),
                iss="accounts.google.com",
            )
        except ValidationError:
            assert True
        else:
            assert False

    def test_name(self):
        serializer = GoogleIdInfo(
            aud=GOOGLE_CLIENT_ID,
            iat=datetime.utcnow().timestamp(),
            exp=(datetime.utcnow() + timedelta(days=1)).timestamp(),
            sub="1",
            iss="accounts.google.com",
            name="user",
        )
        assert isinstance(serializer, GoogleIdInfo)
        assert serializer.username != "user"

    def test_iss(self):
        try:
            GoogleIdInfo(
                aud=GOOGLE_CLIENT_ID,
                iat=datetime.utcnow().timestamp(),
                exp=(datetime.utcnow() + timedelta(days=1)).timestamp(),
                iss="google.com",
                name="user",
            )
        except ValidationError:
            assert True
        else:
            assert False


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
class TestGOCUser:
    """Get or create (GOC) user tests."""

    async def test_get_or_create_user_deactivated_user(
        self, backend_app, single_disabled_user, existing_deactivated_user_id_info
    ):
        try:
            await get_or_create_user(existing_deactivated_user_id_info)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_or_create_user_update_user(
        self, backend_app, single_admin, existing_user_id_info
    ):
        user_object = await get_or_create_user(existing_user_id_info)
        assert user_object.ext_id == existing_user_id_info.sub
        assert user_object.given_name == existing_user_id_info.given_name
        assert user_object.family_name == existing_user_id_info.family_name

    async def test_get_or_create_user_create_user(self, backend_app, google_id_info):
        user_obj = await UserGinoModel.query.where(
            UserGinoModel.ext_id == google_id_info.sub
        ).gino.first()
        assert not user_obj
        user_object = await get_or_create_user(google_id_info)
        assert user_object.ext_id == google_id_info.sub
        assert user_object.given_name == google_id_info.given_name
        assert user_object.family_name == google_id_info.family_name


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
class TestGCUser:
    """Get current (GC) user tests."""

    async def test_get_current_active_user(
        self, backend_app, single_admin_access_token
    ):
        user_object = await get_current_user(single_admin_access_token)
        assert isinstance(user_object, UserGinoModel)

    async def test_get_current_disabled_user(
        self, backend_app, single_disabled_admin_token
    ):
        try:
            await get_current_user(single_disabled_admin_token)
        except HTTPException as ex:
            assert ex.status_code == INACTIVE_EX.status_code
        else:
            assert False

    async def test_get_current_user_bad_token(self, backend_app, bad_access_token):
        try:
            await get_current_user(bad_access_token)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_current_user_no_token(self, backend_app):
        try:
            await get_current_user("")
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
class TestGUserFR:
    """Get user (GU) for refresh tests."""

    async def test_get_active_user_for_refresh(
        self, backend_app, single_admin_refresh_token
    ):
        user_object = await get_user_for_refresh(single_admin_refresh_token)
        assert isinstance(user_object, UserGinoModel)

    async def test_get_disabled_user_for_refresh(
        self, backend_app, single_disabled_refresh_token
    ):
        try:
            await get_user_for_refresh(single_disabled_refresh_token)
        except HTTPException as ex:
            assert ex.status_code == INACTIVE_EX.status_code
        else:
            assert False

    async def test_get_current_user_for_refresh_bad_token(
        self, backend_app, bad_access_token
    ):
        try:
            await get_user_for_refresh(bad_access_token)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_current_user_for_refresh_unknown_token(
        self, backend_app, single_admin_refresh_token, no_refresh_token
    ):
        try:
            await get_user_for_refresh(single_admin_refresh_token)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_current_user_for_refresh_no_token(self, backend_app):
        try:
            await get_user_for_refresh("")
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
async def test_login(backend_app):

    resp = await backend_app.get(
        f"{API_URL_PREFIX}/login", query_string={"state": "qwe"}, allow_redirects=False
    )

    assert resp.status_code == status.HTTP_307_TEMPORARY_REDIRECT


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
async def test_logout(backend_app, single_admin_auth_headers):
    resp = await backend_app.get(
        f"{API_URL_PREFIX}/logout", headers=single_admin_auth_headers
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
async def test_logout_2(backend_app):
    resp = await backend_app.get(f"{API_URL_PREFIX}/logout")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
class TestUserInfo:
    """Authenticated user attributes tests."""

    API_URL = f"{API_URL_PREFIX}/user/info"

    async def test_granted_info(
        self, backend_app, single_admin, single_admin_auth_headers
    ):
        resp = await backend_app.get(self.API_URL, headers=single_admin_auth_headers)
        assert resp.status_code == status.HTTP_200_OK
        assert "data" in resp.json()
        response_data = resp.json()["data"]
        assert "attributes" in response_data
        response_attributes = response_data["attributes"]
        for key in response_attributes:
            if key == "created":
                continue
            assert hasattr(single_admin, key)
            assert response_attributes[key] == getattr(single_admin, key)

    async def test_permitted_info(self, backend_app):
        resp = await backend_app.get(self.API_URL)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
async def test_refresh_access_token(backend_app, single_admin_refresh_token):
    resp = await backend_app.post(
        f"{API_URL_PREFIX}/refresh_access_token",
        query_string={"token": single_admin_refresh_token},
    )
    assert resp.status_code == status.HTTP_200_OK
    resp_data = resp.json()
    assert "access_token" in resp_data
    assert "refresh_token" in resp_data


@pytest.mark.skipif(
    os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
)
async def test_refresh_access_token_with_bad_token(backend_app):
    resp = await backend_app.post(
        f"{API_URL_PREFIX}/refresh_access_token", query_string={"token": "qwe"}
    )
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
