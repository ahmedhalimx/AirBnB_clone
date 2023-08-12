#!/usr/bin/env python3
"""
Defines City class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    A subclass of BaseModel class
    """
    state_id = ""
    name = ""
