import time
from pathlib import Path
from .logger import Logger
from .config import Config
from .process import paralle_process

logger = Logger()
config = Config()

SCOPE_DIRECTORY = config.get["SCOPE_DIRECTORY"]
if SCOPE_DIRECTORY == "" or SCOPE_DIRECTORY == "/" or SCOPE_DIRECTORY == "None":
    raise ValueError("Scope direcotry cannot be empty")

SCOPE_DIRECTORY = Path(str(SCOPE_DIRECTORY))

def main():
    logger.info("Singular started")
    running = True
    while running:
        paralle_process(SCOPE_DIRECTORY)
        logger.info("Sleeping for 15 mins")
        time.sleep(15*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Quitting")
        quit()