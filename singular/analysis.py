from .logger import Logger
from .data_base_manager import DataBase
from .config import Config
from .file import File
from pathlib import Path

logger = Logger()
config = Config()
data_base = DataBase()

class Analyzer:
    def __init__(self):
        self.data_dict = data_base.get()
        self.file_dict = self._file_dict_obj_construct()
    
    def _file_dict_obj_construct(self)->dict:
        file_dict = dict()
        for file_path in self.data_dict.keys():
            try:
                file = File(Path(file_path),_internal_init=True)
                file.sha256 = self.data_dict[file_path]["sha256"]
                file.time_to_process = self.data_dict[file_path]["processing_time"]
                file_dict[file_path] = file
            except FileNotFoundError:
                continue
        return file_dict
    
    def get_duplicates(self):
        duplicates_dict = {}
        file_path_list = list(self.data_dict.keys())
        visited = set()

        for file_path in file_path_list:
            if file_path in visited:
                continue
            file_obj = self.file_dict[file_path]  # type: ignore
            dup_files = [file_path]

            for key in file_path_list:
                if key == file_path or key in visited:
                    continue
                value = self.file_dict[key]
                if file_obj.sha256 == value.sha256:
                    dup_files.append(key)
                    visited.add(key)

            if len(dup_files) > 1:  # Only store if duplicates exist
                duplicates_dict[file_path] = dup_files
                visited.update(dup_files)

        return duplicates_dict
    
    def avg_process_time(self):
        time_to_process_list = [file.time_to_process for file in self.file_dict.values()]
        return sum(time_to_process_list)/len(time_to_process_list)
    
    def total_process_time(self):
        time_to_process_list = [file.time_to_process for file in self.file_dict.values()]
        return sum(time_to_process_list)
    
    
# 2025-12-16 12:22:48,842 - singular.logger - INFO - 0.013630982824791235 avg process time with rust
# 2025-12-16 12:23:35,860 - singular.logger - INFO - 0.026154653661649346 avg process time without rust
# about ~47% faster avg proccess time

# 2025-12-16 12:29:24,485 - singular.logger - INFO - 65.21233367919922 total process time with rust
# 2025-12-16 12:28:09,663 - singular.logger - INFO - 125.20685052871704 total process time without rust
# about ~47% faster total proccess time