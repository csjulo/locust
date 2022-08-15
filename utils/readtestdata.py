import csv
import time
import random

class CsvRead:
    def __init__(self, file):
        try:
            file = open(file)
        except FileNotFoundError:
            print("File not found")

        self.file = file
        self.reader = csv.DictReader(file)

    def read(self):
        # return random.choice(list(self.reader))
        return list(self.reader)
