# models.py

import os
import yaml
from config import Config

class CheatSheet:
    def __init__(self, name, data=None):
        self.name = name
        self.file_path = os.path.join(Config.CHEATSHEETS_FOLDER, f"{self.name}.yaml")
        self.data = data or {}

    def load(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Cheat sheet '{self.name}' not found.")
        with open(self.file_path, 'r') as file:
            self.data = yaml.safe_load(file)
        return self

    def save(self):
        with open(self.file_path, 'w') as file:
            yaml.dump(self.data, file)

    def delete(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    @staticmethod
    def list_all():
        cheatsheets = []
        for file_name in os.listdir(Config.CHEATSHEETS_FOLDER):
            if file_name.endswith('.yaml'):
                cheatsheet_name = os.path.splitext(file_name)[0]
                cheatsheets.append(cheatsheet_name)
        return cheatsheets

