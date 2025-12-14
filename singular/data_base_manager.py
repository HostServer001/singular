from pathlib import Path
from .config import Config
from .utils import _hr_time_stamp

config = Config()

class DataBase:
    def __init__(self) -> None:
        self.data_base_path = config.get["DATA_BASE_PATH"]
        self.data_base_folder = Path(str(self.data_base_folder))
        self._check_db_health()
        self.lazy_load()
    
    def lazy_load(self):
        self.data_base_file = Path(self.data_base_folder/"FileSystemDataBase.json")
        info = self.data_base_file.stat()
        self.data_base_size = info.st_size
        self.last_modified = info.st_mtime
        self.hr_last_modifed = _hr_time_stamp(self.last_modified)

    def _check_db_health(self):
        for child in self.data_base_folder.iterdir():
            if child.is_file and child.name == "FileSystemDataBase.json":
                pass
            else:
                file = open(str(self.data_base_folder/"FileSystemDataBase.json"))
                file.close()
    