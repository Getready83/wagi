import json
import pickle
import sys
import csv
from os import listdir, path


class ReadWrite:
    flag_read = "r"
    flag_write = "w"

    def __init__(self):
        self.content = []

    def read_inner(self, file):
        raise NotImplementedError("None method read_inner")

    def write_inner(self, file):
        raise NotImplementedError("None method write_inner")

    def read(self):
        if "b" not in self.flag_read:
            kwargs = {"encoding": "utf-8"}
        else:
            kwargs = {}

        with open(sys.argv[1], self.flag_read, **kwargs) as file:
            self.read_inner(file)

    def write(self):
        if "b" not in self.flag_write:
            kwargs = {"newline": "", "encoding": "utf-8"}
        else:
            kwargs = {}
        with open(
                sys.argv[2], self.flag_write, **kwargs) as file:
            self.write_inner(file)

    def path(self):
        path.exists(sys.argv[1])
        if not path.exists(sys.argv[1]):
            print(f"Invalid file name or file with this name does not exist "
            f"Files available in this directory are: {listdir()}\n "
            f"directory path is : "
            f"{path.dirname(path.abspath(__file__))}")

    def replacment(self):
        if len(sys.argv) >= 3:
            akcja1 = []
            for n in sys.argv[3:]:
                akcja = n.split(",")
                akcja1.append(akcja)
                for akcja in akcja1:
                    y = akcja[0]
                    x = akcja[1]
                    value = akcja[2]
                    if len(self.content) <= int(y):
                        print("file is to short")
                    elif len(self.content[int(y)]) <= int(x):
                        print("column out of range")
                    else:
                        self.content[int(y)][int(x)] = value


class CsvReaader(ReadWrite):

    def read_inner(self, file):
        reader = csv.reader(file)
        for line in reader:
            self.content.append(line)


class CsvWriter(ReadWrite):

    def write_inner(self, file):
        writer = csv.writer(file)
        writer.writerows(self.content)


class JsonReader(ReadWrite):
    def read_inner(self, file):
        content = file.read()
        print(content)
        self.content = json.loads(content)


class JsonWriter(ReadWrite):
    def write_inner(self, file):
        print(self.content)
        file.write(json.dumps(self.content))


class PickleReaader(ReadWrite):
    flag_read = "rb"

    def read_inner(self, file):
        self.content = pickle.loads(file.read())


class PickleWriter(ReadWrite):
    flag_write = "wb"

    def write_inner(self, file):
        file.write(pickle.dumps(self.content))


file_ext = sys.argv[1].split(".")[-1]
dict_reader = {"csv": CsvReaader, "json": JsonReader, "pickle": PickleReaader}
Reader = dict_reader[file_ext]
file_ext = sys.argv[2].split(".")[-1]
dict_writer = {"csv": CsvWriter, "json": JsonWriter, "pickle": PickleWriter}
Writer = dict_writer[file_ext]


class ReaderWriter(Reader, Writer):
    pass


obj = ReaderWriter()
obj.path()
obj.read()
obj.replacment()
obj.write()
