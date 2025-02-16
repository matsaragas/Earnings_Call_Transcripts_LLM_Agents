from config import Settings
from utils import Utility


class Controller:

    def __init__(self, settings: Settings, retriever):
        self.configs = Utility.load_yaml("./config/config.yaml")