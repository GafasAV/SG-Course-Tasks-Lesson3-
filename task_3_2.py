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


class CSVLoader(object):
    """
    .csv file class
    -csv_load() Load data from file
    -csv_save() Write csv data to file
    """
    @staticmethod
    def csv_load(file):
        data = file.read()

        text = "".join(line.replace(";", " ") for line in data)

        return text

    @staticmethod
    def csv_save(s, file):
        data = s.replace(" ", ";")

        file.write(data)


class JSONLoader(object):
    """
    .json file class
    -json_load() Read data from file
    -json_save() Write json data to file
    """
    @staticmethod
    def json_load(file):
        data = json.load(file)
        s_list = data["rows"]

        text = "\n".join(line for line in s_list)

        return text

    @staticmethod
    def json_save(s, file):
        lines = list(s.split("\n"))

        data = dict()
        data["rows"] = lines

        json.dump(data, file)


class Converter(AbsConverter):
    """
    Converter class, use JSON or CSV read\write methods
    Depending on which file format is specified (csv/json)
    """
    def __init__(self, _from, _to):
        self.src = _from
        self.dst = _to

    def load(self, file):
        if self.src == "csv":
            loader = CSVLoader()
            data = loader.csv_load(file)

        if self.src == "json":
            loader = JSONLoader()
            data = loader.json_load(file)

        return data

    def save(self, s, file):
        if self.dst == "csv":
            saver = CSVLoader()
            saver.csv_save(s, file)

        if self.dst == "json":
            saver = JSONLoader()
            saver.json_save(s, file)

        return result


class ConverterFabric(AbsConverterFabric):

    def create_converter(self, _from, _to):
        converter = Converter(_from, _to)

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
