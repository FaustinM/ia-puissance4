import json
import time


class LogManager:
    def __init__(self, name=None):
        if name:
            self.name = f"logs/{name}.jsonl"
        else:
            self.name = f"logs/{time.time()}.jsonl"

    def openFile(self):
        self.file = open(self.name, "w")
        return self.file

    def closeFile(self):
        self.file.close()

    def saveData(self, data=[]):
        for item in data:
            self.file.write(json.dumps(item) + "\n")
            self.file.flush()
