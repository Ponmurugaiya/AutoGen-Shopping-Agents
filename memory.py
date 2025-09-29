import json
import os

# ----------------------------
# Persistent Memory per Agent
# ----------------------------
class PersistentMemory:
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.memory = json.load(f)
        else:
            self.memory = {}

    def set(self, key, value):
        self.memory[key] = value
        self.save()

    def get(self, key, default=None):
        return self.memory.get(key, default)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.memory, f, indent=2)
