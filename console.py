#!/usr/bin/python3
"""Module for the command line interpreter"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = "(hbnb) "
    cls_map = {
            "BaseModel": BaseModel, "User": User,
            "City": City, "State": State, "City": City,
            "Amenity": Amenity, "Place": Place, "Review": Review
            }

    def emptyline(self):
        """User entered no input"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program at EOF (Ctrl+D)"""
        return True

    def do_create(self, arg):
        """Create a new instance of BaseModel,
        save it, and print the id"""

        if not arg:
            print("** class name missing **")

        else:
            class_name = arg.strip()
            if arg not in HBNBCommand.cls_map:
                print("** class doesn't exist **")
            else:
                new_instance = HBNBCommand.cls_map[class_name]()
                new_instance.save()
                print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""

        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based
        on the class name and id"""

        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representations of instances"""

        args = arg.split()
        obj_list = []

        if not args:
            for key, obj in storage.all().items():
                obj_list.append(str(obj))
            print(obj_list)
            return

        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        for key, obj in storage.all().items():
            if key.split(".")[0] == class_name:
                obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based
        on the class name and id"""

        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]
        instance = storage.all()[key]
        try:
            attr_value = eval(attr_value)
            setattr(instance, attr_name, attr_value)
            instance.save()
        except Exception:
            print("** value missing **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
