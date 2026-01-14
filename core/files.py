from json import load as jload
class Data:
    def __init__(self, filename:str):
        self.file = filename

    def json_read(self):
        with open(f"data/{self.file}.json", "r") as f:
            return jload(f)

    def read(self):
        return open(f"data/{self.file}.txt", "r").read()