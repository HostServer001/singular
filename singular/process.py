from pathlib import Path
from .config import Config
from multiprocessing import Pool
from .utils import _get_chuncked_files,_process_chunk,_get_file_paths,_genrate_hash

config = Config()
SCOPED_DIRECTORY = config.get["SCOPED_DIRECTORY"]
if SCOPED_DIRECTORY == "" or SCOPED_DIRECTORY == "/":
    raise ValueError("Scoped direcotry cannot be empty")

SCOPED_DIRECTORY = Path(str(SCOPED_DIRECTORY))

def paralle_process()->dict:
    chunked_file_list = _get_chuncked_files(SCOPED_DIRECTORY) # type: ignore
    final_dict = {}
    with Pool(5) as p:
        dicts_list = p.map(_process_chunk,chunked_file_list)
        for sub_dict in dicts_list:
            final_dict.update(sub_dict)
    
    return final_dict

def qued_proccess()->dict:
    files = _get_file_paths(SCOPED_DIRECTORY, []) # type: ignore
    final_dict = {}

    for file in files:
        file_hash = _genrate_hash(file)
        final_dict[str(file_hash)] = str(file)

    return final_dict