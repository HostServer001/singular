from pathlib import Path
from .config import Config
from .utils import _hr_time_stamp
import logging

logger = logging.getLogger()
config = Config()
if config.get["DEBUG"] == True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

class DataBase:
    def __init__(self) -> None:
        self.data_base_path = config.get["DATA_BASE_PATH"]
        self.data_base_folder = Path(str(self.data_base_path))
        self._check_db_health()
        self.lazy_load()
    
    def lazy_load(self):
        self.data_base_file = Path(self.data_base_folder/"FileSystemDataBase.json")
        info = self.data_base_file.stat()
        self.data_base_size = info.st_size
        self.last_modified = info.st_mtime
        self.hr_last_modifed = _hr_time_stamp(self.last_modified)
        logger.info("Data base loaded")

    def _check_db_health(self):
        if "FileSystemDataBase.json" in [child.name for child in self.data_base_folder.iterdir()]:
            pass
        else:
            file = open(str(self.data_base_folder/"FileSystemDataBase.json"))
            file.close()
    