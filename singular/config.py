import os
import json
from pathlib import Path

class Config:
    """What? Config class handels configurations for singular"""
    """Why? This class was neccessary to decide the codeflow without users expilict attention.
    Since the whole code base can access the configurations due to this class we dont need to
    define the logic in a linear way and chage every arugument for every internal function for
    evry unique requirements . User will change config every internal function will adapt to 
    that requirement no need to write if else statements for each unique requirements.
    
    """
    def __init__(self):
        "Initialzation of Config"
        #defined parrent folder path and .env file path using the path of config.py (__file__)
        self.config_file_path = "/etc/sigular/singular_config.json"
        # parent_folder = Path(Path(config_file_path).parent)
        # self.env_path = str(parent_folder/".env")
        self.default_env_dict = {
            "DATA_BASE_PATH": "/var/lib/singular",
            "SCOPE_DIRECTORY": os.path.expanduser("~"),
            "LOG_FILE":"/var/log/singular",
            "ACCESS_HIDDEN_FILES": "False",
            "DEBUG": "False"
        }
        try:
            self.config = json.load(open(self.config_file_path,"r"))
        except FileNotFoundError:
            os.makedirs("/etc/singular",exist_ok=True)
            file = open("/etc/singular/singular_config.json","w")
            json.dump(self.default_env_dict,file,indent=4)
            file.close()

        #load .env, load config, check if configs are useable if not fix
        # load_dotenv(self.env_path)
        self._load_config()
        self._config_health_fix()

    def _load_config(self):
        """What? Loads the configs"""
        """Why? Yes I could have just wrote all the variables in __init__ but 
        if a config is chaged while run started then i have have to load these things again
        but if these variables are in __init__ this means we are re initializing the whole class,
        this in my opinion was risky and inconsistent thats why this approach
        """
        file = open(self.config_file_path,"r")
        config_dict = json.load(file)
        file.close()
        self.data_base_path = config_dict["DATA_BASE_PATH"]
        self.scope_diretory = config_dict["SCOPE_DIRECTORY"]
        self.log_file = config_dict["LOG_FILE"]
        self.access_hidden_files = config_dict["ACCESS_HIDDEN_FILES"]
        self.debug = config_dict["DEBUG"]

    def _config_health_fix(self):
        """What? Checking health of config"""
        """Why? Ofcource health checks are importnat :)"""
        path = Path(self.data_base_path or "")
        if not path.is_dir():
            self._change_config("DATA_BASE_PATH", self.default_env_dict["DATA_BASE_PATH"])
        for key in self.default_env_dict.keys():
            for value in self.get.values():
                if self.get.get(key,None) == None or value == None:
                    self._change_config(key, self.default_env_dict.get(key))
        if not Path(self.log_file).exists():#type:ignore
            file = open(self.log_file,"w")#type:ignore
            file.close()
    
    def set_key(self,key,value):
        file = open(self.config_file_path,"r")
        config_dict = json.load(file)
        file.close()
        config_dict[key] = value
        file = open(self.config_file_path,"w")
        json.dump(config_dict,file,indent=4)
        file.close
        
    def _change_config(self, key, value):
        """What? Chanegs the config"""
        """Why? Code should be abel to change the configs on user demand :)"""
        self.set_key(key, value)
        self._load_config()  # reload values only

    @property
    def get(self):
        """What? Returns the configurations dict"""
        """Why? What a Config class which cant dosent has method to retirve th configurations :)"""
        return {
            "DATA_BASE_PATH": self.data_base_path,
            "SCOPE_DIRECTORY": self.scope_diretory,
            "LOG_FILE": self.log_file,
            "ACCESS_HIDDEN_FILES": self.access_hidden_files,
            "DEBUG": self.debug
        }
