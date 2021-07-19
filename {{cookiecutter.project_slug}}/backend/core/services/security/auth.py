# -*- coding: utf-8 -*-
"""Authentication system."""

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from jose import JWTError

from core.config import LOGIN_ENDPOINT, SWAP_TOKEN_ENDPOINT
from core.database import UserGinoModel
from core.schemas import AccessToken, GoogleIdInfo, RefreshToken
from core.utils import CREDENTIALS_EX, INACTIVE_EX

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=LOGIN_ENDPOINT, tokenUrl=SWAP_TOKEN_ENDPOINT
)


async def get_or_create_user(id_info: GoogleIdInfo):
    """Get/Update or Create new user."""
    return await UserGinoModel.insert_or_update_by_ext_id(
        sub=id_info.sub,
        username=id_info.username,
        family_name=id_info.family_name,
        given_name=id_info.given_name,
        full_name=id_info.name,
    )


async def get_user_for_refresh(token: str):
    try:
        token_info = RefreshToken.decode_and_create(token=token)
        user = await UserGinoModel.get(token_info.id)
        if user is None or user.disabled:
            raise INACTIVE_EX
        token_valid = await user.token_is_valid(token)
        if not token_valid:
            raise CREDENTIALS_EX
    except (JWTError, ValueError):
        raise CREDENTIALS_EX
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):  # noqa: B008
    """Validate token and get user db model instance.

    Example:
        @auth_router.get(f"{SUCCESS_ROUTE}", response_model=UserDBModel)
        @version(1)
        async def read_users_me(  # noqa: D103
            current_user: UserDBModel = Depends(get_current_user),  # noqa: B008
        ):
            return current_user
    """
    try:
        token_info = AccessToken.decode_and_create(token=token)
        user = await UserGinoModel.get(token_info.id)
        if user is None or user.disabled:
            raise INACTIVE_EX
    except (JWTError, ValueError):
        raise CREDENTIALS_EX
    return user
