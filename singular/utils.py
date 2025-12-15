import time
import json
import hashlib
from pathlib import Path
from multiprocessing import Pool
from datetime import datetime
from .config import Config

config = Config()

def _get_file_paths(
        SCOPE_DIRECTORY:Path,
        list_to_store:list
        )->list:
    "Implementation of recursive file listing"  
    for item in SCOPE_DIRECTORY.iterdir():
        try:
            if item.is_dir() and item.name in ["pro_py"]:
                continue
            if item.is_dir():
                if item.name.startswith(".") and config.get["ACCESS_HIDDEN_FILES"] == "False":
                    continue
                _get_file_paths(item,list_to_store)
            
            elif item.is_file():
                if item.name == "FileSystemDataBase.json":
                    continue
                if item.name.startswith(".") and config.get["ACCESS_HIDDEN_FILES"] == "False":
                    continue
                list_to_store.append(item.resolve())
        
        except PermissionError:
            continue
    
    return list_to_store

def _genrate_hash(file:Path)->str:
    with open(str(file),"rb") as file_content:
        hash = hashlib.sha256(file_content.read())
        return hash.hexdigest()

# def _process_chunk(chunk:list)->dict:
#     hash_dict = {str(_genrate_hash(file)):str(file) for file in chunk}
#     return hash_dict

# def _process_chunk(chunk:list)->dict:
#     final_dict = dict()
#     for path in chunk:
#         file = File(path)
#         final_dict.update(file.dict)
#     return final_dict



def _get_chuncked_files(SCOPE_DIRECOTRY:Path)->list:
    files_to_hash = []
    _get_file_paths(SCOPE_DIRECOTRY,files_to_hash)
    file_list = [
        files_to_hash[n:n+round(len(files_to_hash)/4)] 
        for n in range(
            0,
            len(files_to_hash),
            round(len(files_to_hash)/4)
            )
        ]
    return file_list

# def paralle_process()->dict:
#     chunked_file_list = _get_chuncked_files(PARENT_FOLDER)
#     final_dict = {}
#     with Pool(5) as p:
#         dicts_list = p.map(_process_chunk,chunked_file_list)
#         for sub_dict in dicts_list:
#             final_dict.update(sub_dict)
    
#     return final_dict

# def qued_proccess()->dict:
#     files = _get_file_paths(PARENT_FOLDER, [])
#     final_dict = {}

#     for file in files:
#         file_hash = _genrate_hash(file)
#         final_dict[str(file_hash)] = str(file)

#     return final_dict

def metrics(
        qued_process: tuple,
        paralle_process: tuple,
        length_final_dict: int
    ):
    """
    qued_process: (result_dict, elapsed_time)
    paralle_process: (result_dict, elapsed_time)
    length_final_dict: number of total hashes produced
    """

    # unpack times
    q1, q2 = qued_process
    p1, p2 = paralle_process

    qued_process_time = q2-q1
    paralle_process_time = p2-p1

    # time taken
    print(f"Qued process took {qued_process_time/60} min")
    print(f"Parallel process took {paralle_process_time/60} min")


    if paralle_process_time < qued_process_time:
        improvement = ((qued_process_time - paralle_process_time) / qued_process_time) * 100
        print(f"Parallel process outperformed Qued by {improvement:.2f}%")
    else:
        slowdown = ((paralle_process_time - qued_process_time) / qued_process_time) * 100
        print(f"Parallel process was slower than Qued by {slowdown:.2f}%")


    qued_hps = length_final_dict / qued_process_time
    parallel_hps = length_final_dict / paralle_process_time

    print(f"Qued process speed: {qued_hps} hashes/sec")
    print(f"Parallel process speed: {parallel_hps} hashes/sec")


def dump_dict_to_json(data: dict, output_file: str):
    """
    Dump a dictionary to a JSON file with indent=4.
    Converts Path objects to strings for serialization.
    """
    # Convert Path objects to strings

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Dictionary dumped to {output_file}")

def _hr_time_stamp(time_stamp)->str:
        time_stamp = datetime.fromtimestamp(time_stamp)
        string = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        return str(string)