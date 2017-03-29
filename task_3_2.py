from abc import ABC, abstractmethod
import json

__author__ = "Andrew Gafiychuk"


class AbsConverterFabric(ABC):
    """
    Converter Fabric Interface
    """
    @abstractmethod
    def create_converter(self, _from, _to):
        raise NotImplemented


class AbsConverter(ABC):
    """
    Converter Interface
    """
    @abstractmethod
    def load(self, file):
        raise NotImplemented

    @abstractmethod
    def save(self, s, file):
        raise NotImplemented


class AbsLoader(ABC):
    """
    Format file loader interface
    """
    @abstractmethod
    def load_from(file):
        raise NotImplemented

    @abstractmethod
    def save_to(s, file):
        raise NotImplemented


class CSVLoader(AbsLoader):
    """
    .csv file class
    -csv_load() Load data from file
    -csv_save() Write csv data to file
    """
    @staticmethod
    def load_from(file):
        data = file.read()

        text = "".join(line.replace(";", " ") for line in data)

        return text

    @staticmethod
    def save_to(s, file):
        data = s.replace(" ", ";")

        file.write(data)


class JSONLoader(AbsLoader):
    """
    .json file class
    -json_load() Read data from file
    -json_save() Write json data to file
    """
    @staticmethod
    def load_from(file):
        data = json.load(file)
        s_list = data["rows"]

        text = "\n".join(line for line in s_list)

        return text

    @staticmethod
    def save_to(s, file):
        lines = list(s.split("\n"))

        data = dict()
        data["rows"] = lines

        json.dump(data, file)


class Converter(AbsConverter):
    """
    Converter class, use JSON or CSV read\write methods
    Depending on which file format is specified (csv/json)
    """
    def __init__(self, loader, saver):
        self._loader = loader
        self._saver = saver

    def load(self, sfile):
        data = self._loader.load_from(sfile)

        return data

    def save(self, s, file):
        self._saver.save_to(s, file)


class ConverterFabric(AbsConverterFabric):

    _format_handler = {"csv": CSVLoader, "json": JSONLoader}

    def create_converter(self, _from, _to):

        if _from in self._format_handler.keys():
            loader = self._format_handler[_from]
        if _to in self._format_handler.keys():
            saver = self._format_handler[_to]

        converter = Converter(loader, saver)

        return converter


if __name__ == "__main__":
    fab = ConverterFabric()
    converter1 = fab.create_converter("csv", "json")
    converter2 = fab.create_converter("json", "csv")

    with open('csv.txt', 'r') as file:
        result = converter1.load(file)
        print(result)

    print()

    with open('json.txt', 'w') as file:
        converter1.save(result, file)

    with open('json.txt', 'r') as file:
        result = converter2.load(file)
        print(result)

    with open('csv.txt', 'w') as file:
        converter2.save(result, file)

    fab = ConverterFabric()
    converter1 = fab.create_converter('csv', 'json')
    converter2 = fab.create_converter('json', 'csv')

    string = 'Joe Doe Green 77'

    with open('json.txt', 'w') as file:
        converter1.save(string, file)

    print()

    with open('json.txt', 'r') as file:
        result = converter2.load(file)
        print(result)

    with open('csv.txt', 'w') as file:
        converter2.save(result, file)