#!/usr/bin/python3
"""Defines the HBnB console."""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def strtok(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [ch.strip(",") for ch in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            token = [ch.strip(",") for ch in lexer]
            token.append(brackets.group())
            return token
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        token = [ch.strip(",") for ch in lexer]
        token.append(curly_braces.group())
        return token


class HBNBCommand(cmd.Cmd):
    """Defines the HBnB command line interface."""

    prompt = "(hbnb) "
    valid_choices = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
            }

    def emptyline(self):
        """continue when receiving an emptyline."""
        pass

    def quit(self, arg):
        """Exits the program."""
        return True

    def EOF(self, arg):
        """Exit on reciving EOF signal"""
        print("")
        return True

    def create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Creates a new class instance and prints its id.
        """
        try:
            if not line:
                raise SyntaxError()
            attributes = line.split(" ")

            kwargs = {}
            for i in range(1, len(attributes)):
                key, value = tuple(attributes[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(attributes[0])()
            else:
                obj = eval(attributes[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance
        by providing it's id.
        """
        argument = strtok(arg)
        obj_dict = storage.all()
        if len(argument) == 0:
            print("** class name missing **")
        elif argument[0] not in HBNBCommand.valid_choices:
            print("** class doesn't exist **")
        elif len(argument) == 1:
            print("** instance id missing **")
        elif f"{argument[0]}.{argument[1]}" not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict[f"{argument[0]}.{argument[1]}"]

    def destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argument = strtok(arg)
        obj_dict = storage.all()
        if len(argument) == 0:
            print("** class name missing **")
        elif argument[0] not in HBNBCommand.valid_choices:
            print("** class doesn't exist **")
        elif len(argument) == 1:
            print("** instance id missing **")
        elif f"{argument[0]}.{argument[1]}" not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict[f"{argument[0]}.{argument[1]}"]
            storage.save()

    def all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argument = strtok(arg)
        if len(argument) > 0 and argument[0] not in HBNBCommand.valid_choices:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argument) > 0 and argument[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argument) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argument = strtok(arg)
        count = 0
        for obj in storage.all().values():
            if argument[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance by it's id with adding or updating
        a given attribute key/value pair or dictionary."""
        argument = strtok(arg)
        obj_dict = storage.all()

        if len(argument) == 0:
            print("** class name missing **")
            return False

        if argument[0] not in HBNBCommand.valid_choices:
            print("** class doesn't exist **")
            return False

        if len(argument) == 1:
            print("** instance id missing **")
            return False

        if f"{argument[0]}.{argument[1]}" not in obj_dict.keys():
            print("** no instance found **")
            return False

        if len(argument) == 2:
            print("** attribute name missing **")
            return False

        if len(argument) == 3:
            try:
                type(eval(argument[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argument) == 4:
            object = obj_dict[f"{argument[0]}.{argument[1]}"]
            if argument[2] in object.__class__.__dict__.keys():
                valtype = type(object.__class__.__dict__[argument[2]])
                object.__dict__[argument[2]] = valtype(argument[3])
            else:
                object.__dict__[argument[2]] = argument[3]
        elif type(eval(argument[2])) == dict:
            object = obj_dict[f"{argument[0]}.{argument[1]}"]
            for key, value in eval(argument[2]).items():
                if (key in object.__class__.__dict__.keys() and
                        type(object.__class__.__dict__[key]) in
                        {str, int, float}):
                    valtype = type(object.__class__.__dict__[key])
                    object.__dict__[key] = valtype(value)
                else:
                    object.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()

