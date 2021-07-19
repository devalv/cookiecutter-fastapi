# -*- coding: utf-8 -*-
"""Project database configuration."""

from .models import db
from .models.security import TokenInfo as TokenInfoGinoModel
from .models.security import User as UserGinoModel

__all__ = ["UserGinoModel", "TokenInfoGinoModel", "db"]
