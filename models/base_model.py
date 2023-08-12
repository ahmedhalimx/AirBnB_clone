#!/usr/bin/env python3
from datetime import datetime
from uuid import uuid4
import models

"""
Parent class to all classes in the AirBnB clone project
"""


class BaseModel():
    """Parent class for AirBnB clone project
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize attributes: uuid4, dates when class was created/updated
        """
        if kwargs:
            for key, value in kwargs.items():
                if "created_at" == key:
                    self.created_at = datetime.strptime(kwargs["created_at"],
                                                        '%Y-%m-%dT%H:%M:%S.%f')
                elif "updated_at" == key:
                    self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                        '%Y-%m-%dT%H:%M:%S.%f')
                elif "__class__" == key:
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        Return class name, id, and the dictionary
        """
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")

    def __repr__(self):
        """
        returns string repr
        """
        return (self.__str__())

    def save(self):
        """
        Instance method to:
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Return dictionary of BaseModel with string formats of times
        """
        dic = self.__dict__.copy()
        dic["created_at"] = self.created_at.isoformat()
        dic["updated_at"] = self.updated_at.isoformat()
        dic["__class__"] = self.__class__.__name__
        return dic
