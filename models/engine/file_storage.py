#!/usr/bin/python3
"""Defines the class FileStorage"""
import json


class FileStorage:
    """Serializes instances to a JSON file
    and deserializes JSON file to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj
        with key <obj class name>.id"""
        key = "{}.{}".format(
                obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the
        JSON file (path: __file_path)"""
        serialized = {
                key: obj.to_dict() for key, obj in self.__objects.items()}

        with open(self.__file_path, 'w', encoding="utf-8") as file:
            json.dump(serialized, file)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        try:
            with open(self.__file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
            for key, value in data.items():
                class_name, obj_id = key.split(".")
                class_name = class_name.split('"')[0]
                obj_cls = eval(class_name)
                new_obj = obj_cls(**value)
                self.__objects[key] = new_obj

        except FileNotFoundError:
            pass