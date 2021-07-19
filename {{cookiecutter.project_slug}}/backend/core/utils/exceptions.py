# -*- coding: utf-8 -*-
"""Project exceptions."""

from fastapi import HTTPException, status

_headers = {"WWW-Authenticate": "Bearer"}

CREDENTIALS_EX = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers=_headers,
)

INACTIVE_EX = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user", headers=_headers
)


OAUTH2_EX = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to get google OAuth data. Try to reload the page.",
    headers=_headers,
)


NOT_IMPLEMENTED_EX = HTTPException(
    status_code=status.HTTP_501_NOT_IMPLEMENTED, headers=_headers
)

NOT_AN_OWNER = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not an owner.",
    headers=_headers,
)
