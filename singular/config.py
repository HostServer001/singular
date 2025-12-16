import os
from pathlib import Path
from dotenv import load_dotenv, set_key

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
        config_file_path = __file__
        parent_folder = Path(Path(config_file_path).parent)
        self.env_path = str(parent_folder/".env")

        #load .env, load config, check if configs are useable if not fix
        load_dotenv(self.env_path)
        self.default_env_dict = {
            "DATA_BASE_PATH": f"{str(parent_folder/"data_base")}",
            "SCOPE_DIRECTORY": f"/home/{os.getlogin()}",
            "LOG_FILE":f"{str(Path(parent_folder)/"data_base"/"singular.log")}",
            "ACCESS_HIDDEN_FILES": "False",
            "DEBUG": "False"
        }
        self._load_config()
        self._config_health_fix()

    def _load_config(self):
        """What? Loads the configs"""
        """Why? Yes I could have just wrote all the variables in __init__ but 
        if a config is chaged while run started then i have have to load these things again
        but if these variables are in __init__ this means we are re initializing the whole class,
        this in my opinion was risky and inconsistent thats why this approach
        """
        self.data_base_path = os.getenv("DATA_BASE_PATH")
        self.scope_diretory = os.getenv("SCOPE_DIRECTORY")
        self.log_file = os.getenv("LOG_FILE")
        self.access_hidden_files = os.getenv("ACCESS_HIDDEN_FILES")
        self.debug = os.getenv("DEBUG")

    def _config_health_fix(self):
        """What? Checking health of config"""
        """Why? Ofcource health checks are importnat :)"""
        path = Path(self.data_base_path or "")
        if not path.is_dir():
            self._change_config("DATA_BASE_PATH", self.default_env_dict["DATA_BASE_PATH"])
        for key in self.default_env_dict.keys():
            for value in self.get.values():
                if self.get.get(key,None) == None or value == "None":
                    self._change_config(key, self.default_env_dict.get(key))
        if not Path(self.log_file).exists():#type:ignore
            file = open(self.log_file,"w")#type:ignore
            file.close()

    def _change_config(self, key, value):
        """What? Chanegs the config"""
        """Why? Code should be abel to change the configs on user demand :)"""
        set_key(self.env_path, key, value)
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
