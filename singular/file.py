from pathlib import Path
from .utils import _hr_time_stamp
import hashlib

class File:
    def __init__(self,file_path:Path) -> None:
        self.path = file_path
        info = self.path.stat()
        self.data_base_size = info.st_size
        self.last_modified = info.st_mtime
        self.hr_last_modifed = _hr_time_stamp(self.last_modified)
        file = open(str(self.path),"rb")
        self.sha256 = hashlib.sha256(file.read())
        file.close()
    
    @property
    def dict(self):
        return {
            "path": str(self.path),
            "size": self.data_base_size,
            "last_modified": self.last_modified,
            "hr_last_modified": self.hr_last_modifed,
            "sha256": self.sha256,
        }