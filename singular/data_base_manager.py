from pathlib import Path
from .config import Config
from .utils import _hr_time_stamp
from .logger import Logger
import json

logger = Logger()
config = Config()

class DataBase:
    def __init__(self) -> None:
        logger.info(str(config.get))
        self.data_base_path = config.get["DATA_BASE_PATH"]
        logger.info(f"DATA_BASE_PATH  we got {self.data_base_path}")
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
        try:
            if "FileSystemDataBase.json" in [child.name for child in self.data_base_folder.iterdir()]:
                pass
            else:
                file = open(str(self.data_base_folder/"FileSystemDataBase.json"),"w")
                json.dump(dict(),file)
                file.close()
        except FileNotFoundError as e:
            logger.error(str(e))
            quit()

    
    def get(self)->dict:
        db = open(str(self.data_base_file),"r")
        db_dict = json.load(db)
        db.close()
        return db_dict
    
    def set_key(self,key,value):
        db = open(self.data_base_file,"r")
        db_dict = json.load(db)
        db.close()
        
        db_dict[key] = value
        
        db = open(self.data_base_file,"w")
        json.dump(db_dict,db,indent=4)
        db.close()
        self.lazy_load()

        logger.info(f"Succefull key insertion : {key}")