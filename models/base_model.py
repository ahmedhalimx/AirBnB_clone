#!/usr/bin/env python3
"""
Base class for all the other classes
"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel():
    """Parent class for AirBnB clone project"""

    def __init__(self, *args, **kwargs):
        """
        Initialize essintial attributes:
        uuid4, dates when class was created/updated
        """
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f")
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value

    def __str__(self):
        """
        Return class name, id, and the dictionary
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def __repr__(self):
        """
        Returns a repr string
        """
        return self.__str__()

    def save(self):
        """
        Updates the updated_at datetime attribute
        and stores it by calling storage.save()
        """
        self.updated_at = datetime.isoformat(datetime.utcnow()))
        models.storage.save(self)

    def to_dict(self):
        """
        Returns the dictionary representation of BaseModel
        """
        obj_to_dict={}
        obj_to_dict["__class__"]=self.__class__.__name__

        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                obj_to_dict[key]=value.isoformat()
            else:
                obj_to_dict[key]=value
        return obj_to_dict
