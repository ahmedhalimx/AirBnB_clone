#!/usr/bin/env python3
"""
Defines Review class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    A subclass of BaseModel class
    """
    place_id = ""
    user_id = ""
    text = ""
