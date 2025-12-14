from pathlib import Path
from .config import Config
from multiprocessing import Pool,cpu_count
from .utils import _get_chuncked_files,_process_chunk,_get_file_paths,_genrate_hash
import logging


config = Config()
logger = logging.getLogger()

SCOPE_DIRECTORY = config.get["SCOPE_DIRECTORY"]
if SCOPE_DIRECTORY == "" or SCOPE_DIRECTORY == "/" or SCOPE_DIRECTORY == "None":
    raise ValueError("Scope direcotry cannot be empty")

SCOPE_DIRECTORY = Path(str(SCOPE_DIRECTORY))

if config.get["DEBUG"] == "True":
    logger.setLevel(logging.DEBUG)



def paralle_process()->dict: #type:ignore
    try:
        chunked_file_list = _get_chuncked_files(SCOPE_DIRECTORY) # type: ignore
        final_dict = {}
        with Pool(cpu_count()) as p:
            dicts_list = p.map(_process_chunk,chunked_file_list)
            for sub_dict in dicts_list:
                final_dict.update(sub_dict)
        return final_dict
    except Exception as e:
        logger.error(e)
        

def qued_proccess()->dict: #type:ignore
    try:
        files = _get_file_paths(SCOPE_DIRECTORY, []) # type: ignore
        final_dict = {}

        for file in files:
            file_hash = _genrate_hash(file)
            final_dict[str(file_hash)] = str(file)

        return final_dict
    except Exception as e:
        logger.error(e)