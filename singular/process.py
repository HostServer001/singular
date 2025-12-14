from pathlib import Path
from .config import Config
from multiprocessing import Pool,cpu_count
from .utils import _get_chuncked_files
from .logger import Logger
from .data_base_manager import DataBase
from .file import File

config = Config()
logger = Logger()
data_base = DataBase()

def _process_chunk(chunk:list)->dict:
    final_dict = dict()
    for path in chunk:
        file = File(path)
        final_dict.update(file.dict)
    return final_dict



def _clean_chunk(file_list)->list:
    db_dict = data_base.get()
    registered_files = db_dict.keys()
    clean_list = []
    for file in file_list:
        info = file.stat()
        if file not in registered_files:
            clean_list.append(file)
        elif file in registered_files and (info.st_size != db_dict[file]["size"] or info.st_mtime != db_dict[file]["last_modified"]):
            clean_list.append(file)
    return clean_list


def paralle_process(SCOPE_DIRECTORY): #type:ignore
    try:
        chunked_file_list = _clean_chunk(_get_chuncked_files(SCOPE_DIRECTORY)) # type: ignore
        final_dict = {}
        with Pool(cpu_count()) as p:
            dicts_list = p.map(_process_chunk,chunked_file_list)
            for sub_dict in dicts_list:
                final_dict.update(sub_dict)
        for key in final_dict.keys():
            data_base.set_key(key,final_dict.get(key))
        # return final_dict
    except Exception as e:
        logger.error(f"Error in paralle process : {e}")
        

# def qued_proccess()->dict: #type:ignore
#     try:
#         files = _get_file_paths(SCOPE_DIRECTORY, []) # type: ignore
#         final_dict = _process_chunk(files)
#         return final_dict
#     except Exception as e:
#         logger.error(f"Error in qued process : {e}")