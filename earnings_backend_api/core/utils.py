import yaml

class Utility:

    @staticmethod
    def load_yaml(filepath: str) -> dict:
        with open(filepath, "r") as file:
            return yaml.safe_load(file)

