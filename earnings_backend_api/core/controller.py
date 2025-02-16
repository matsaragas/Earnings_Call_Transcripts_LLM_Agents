from config import Settings
from core.utils import Utility


class Controller:

    def __init__(self, settings: Settings):
        self.configs = Utility.load_yaml("./config/config.yaml")