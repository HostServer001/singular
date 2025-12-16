import time
from pathlib import Path
from .logger import Logger
from .config import Config
from .process import paralle_process
from .analysis import Analyzer
# import rustimport.import_hook
# from . import file_io # pyright: ignore[reportAttributeAccessIssue]

# print(file_io.square(2))
# quit()


logger = Logger()
config = Config()
analyser = Analyzer()

SCOPE_DIRECTORY = config.get["SCOPE_DIRECTORY"]
if SCOPE_DIRECTORY == "" or SCOPE_DIRECTORY == "/" or SCOPE_DIRECTORY == "None":
    raise ValueError("Scope direcotry cannot be empty")

SCOPE_DIRECTORY = Path(str(SCOPE_DIRECTORY))

def main():
    logger.info("Singular started")
    running = True
    while running:
        paralle_process(SCOPE_DIRECTORY)
        logger.info(str(analyser.avg_process_time()))
        logger.info(str(analyser.total_process_time()))
        # logger.info(str(analyser.get_duplicates()))
        logger.info("Sleeping for 1 mins")
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Quitting")
        quit()