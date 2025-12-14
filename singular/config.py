import os
from pathlib import Path
from dotenv import load_dotenv, set_key, find_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.default_env_dict = {
            "DATA_BASE_PATH": "/home/jvk/hashing_algo/singular/data_base",
            "SCOPE_DIRECOTRY": "None",
            "ACCESS_HIDDEN_FILES": "False",
            "DEBUG": "False"
        }
        self._load_config()
        self._config_health_fix()

    def _load_config(self):
        self.data_base_path = os.getenv("DATA_BASE_PATH")
        self.scope_diretory = os.getenv("SCOPE_DIRECOTRY")
        self.access_hidden_files = os.getenv("ACCESS_HIDDEN_FILES")
        self.debug = os.getenv("DEBUG")

    def _config_health_fix(self):
        """Checking health of config"""
        path = Path(self.data_base_path or "")
        if not path.is_dir():
            self._change_config("DATA_BASE_PATH", self.default_env_dict["DATA_BASE_PATH"])
        for key, value in self.get.items():
            if value is None:
                self._change_config(key, self.default_env_dict.get(key))

    def _change_config(self, key, value):
        set_key(find_dotenv(), key, value)
        self._load_config()  # reload values only

    @property
    def get(self):
        return {
            "DATA_BASE_PATH": self.data_base_path,
            "SCOPE_DIRECOTRY": self.scope_diretory,
            "ACCESS_HIDDEN_FILES": self.access_hidden_files,
            "DEBUG": self.debug
        }
