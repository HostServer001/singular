import time
import typer
from pathlib import Path
from .logger import Logger
from .config import Config
from .process import paralle_process
from multiprocessing import Pool, cpu_count
from .analysis import Analyzer
from typing_extensions import Annotated
from typing import Literal
from .cli_texts import (
    daemon_cmd_help,
    config_cmd_help,
    set_opt_help,
    default_opt_help,
    analysis_cmd_help
)
# import rustimport.import_hook
# from . import file_io # pyright: ignore[reportAttributeAccessIssue]

# print(file_io.square(2))
# quit()


logger = Logger()
config_class = Config()
analyser = Analyzer()
app = typer.Typer()

SCOPE_DIRECTORY = config_class.get["SCOPE_DIRECTORY"]
if SCOPE_DIRECTORY == "" or SCOPE_DIRECTORY == "/" or SCOPE_DIRECTORY == "None":
    raise ValueError("Scope direcotry cannot be empty")

SCOPE_DIRECTORY = Path(str(SCOPE_DIRECTORY))

@app.command(help=daemon_cmd_help)
def daemon():
    logger.info("Singular started")
    # Create pool ONCE and reuse it
    with Pool(cpu_count()) as pool:
        while True:
            logger.info(str(cpu_count()))
            paralle_process(SCOPE_DIRECTORY, pool)
            logger.info("Sleeping for 1 min")
            time.sleep(60)

@app.command(help=config_cmd_help)
def config(
    set_: Annotated[list[str], typer.Option("--set", "-s", help=set_opt_help)],
    default_: Annotated[bool, typer.Option("--default", "-d", help=default_opt_help)] = False
):
    if default_:
        for key, value in config_class.default_env_dict.items():
            config_class._change_config(key, value)
    else:
        for pair in set_:
            key, value = pair.split("=")
            config_class._change_config(key, value.strip('"'))

@app.command(help=analysis_cmd_help)
def analysis():
    logger.info("Starting analysis...")
    analyzer = Analyzer()

    duplicates = analyzer.get_duplicates()
    if duplicates:
        logger.info("Duplicate files detected:")
        for root_file, dup_list in duplicates.items():
            file_names = [Path(f).name for f in dup_list]
            logger.info(f"{Path(root_file).name}: {', '.join(file_names)}")
    else:
        logger.info("No duplicate files found.")

    try:
        avg_time = analyzer.avg_process_time()
        logger.info(f"Average processing time: {avg_time:.2f} seconds")
    except ZeroDivisionError:
        logger.warning("No files available to calculate average processing time.")

    total_time = analyzer.total_process_time()
    logger.info(f"Total processing time: {total_time:.2f} seconds")

    logger.info("Analysis complete.")



# def main():
#     logger.info("Singular started")
#     running = True
#     while running:
#         paralle_process(SCOPE_DIRECTORY)
#         logger.info(str(analyser.avg_process_time()))
#         logger.info(str(analyser.total_process_time()))
#         # logger.info(str(analyser.get_duplicates()))
#         logger.info("Sleeping for 1 mins")
#         time.sleep(60)

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        logger.info("Quitting")