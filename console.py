#!/usr/bin/env python3
"""
Defines hbnb Command line interface
"""
import cmd
import sys
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.city import City
from models.amenity import Amenity
from models import storage
import json
import re
import shlex


class HBNBCommand(cmd.Cmd):
    """The HBNB command line interface"""

    prompt = '(hbnb) '
    classes = [
            'BaseModel',
            'User',
            'Place',
            'Review',
            'State',
            'City',
            'Amenity'
            ]

    def emptyline(self):
        """Skip empty line"""
        pass

    def do_quit(self, line):
        """Exit the program"""
        sys.exit()

    def do_EOF(self, line):
        """Quit when reciving EOF"""
        sys.exit()

    def do_create(self, line):
        '''Creates an instance of BaseModel, saves it and print its id'''
        command = self.parseline(line)[0]
        if command is None:
            print('** class name missing **')
        elif not (command in self.classes):
            print('** class doesn\'t exist **')
        else:
            new_instance = eval(command)()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, line):
        '''Prints the string representation of an instance
        based on the class name and id'''
        command = self.parseline(line)[0]
        arg = self.parseline(line)[1]
        if command is None:
            print("** class name is missing **")

        elif not (command in self.classes):
            print("** class doesn't exist **")
        elif arg == '':
            print("** instance id missing **")
        else:
            inst = storage.all().get(command+'.'+arg)
            if inst is None:
                print("** no instance found **")
            else:
                print(inst)

    def do_destroy(self, line):
        '''Deletes an instance based on its id and name'''
        command = self.parseline(line)[0]
        arg = self.parseline(line)[1]
        if command is None:
            print("** class name is missing **")
        elif not (command in self.classes):
            print("** class doesn't exist **")
        elif arg == '':
            print("** instance id missing **")
        else:
            inst = storage.all().get(command+'.'+arg)
            if inst is None:
                print("** no instance found **")
            else:
                del storage.all()[command+'.'+arg]
                storage.save()

    def do_all(self, line):
        '''Prints all instances'''
        base_models_collection = storage.all()
        model = self.parseline(line)[0]
        lst = []
        if model is None:
            for i in base_models_collection.values():
                lst.append(str(i))
            print(lst)
        elif not (model in self.classes):
            print("** class doesn't exist **")
        else:
            for i in base_models_collection:
                if i.startswith(model):
                    lst.append(str(base_models_collection[i]))
            print(lst)

    def do_update(self, line):
        "Updates an instance based on it's name and id"

        model = self.parseline(line)[0]
        attributes = self.parseline(line)[1]
        if not (attributes is None):
            attributes = shlex.split(attributes)
            inst = attributes[0]
            instnf = storage.all().get(model+'.'+inst)
        if model is None:
            print("** class name missing **")
        elif (not (model in self.classes)):
            print("** class doesn't exist **")
        elif inst == '':
            print("** instance id missing **")
        elif instnf is None:
            print("** instance not found **")
        elif len(attributes) < 2:
            print("** attribute name missing **")
        elif len(attributes) < 3:
            print("** value missing **")
        else:
            if attributes[2].isdigit():
                attributes[2] = int(attributes[2])
            elif attributes[2].replace('.', '', 1).isdigit():
                attributes[2] = float(attributes[2])
            setattr(instnf, attributes[1], attributes[2])
            storage.save()

    def get_instances(self, instance=''):
        objects = storage.all()
        lst = []
        if instance:
            for key, value in objects.items():
                if key.startswith(instance):
                    lst.append(str(value))
        else:
            for key, value in objects.items():
                lst.append(str(v))
        return lst


if __name__ == '__main__':
    HBNBCommand().cmdloop()
