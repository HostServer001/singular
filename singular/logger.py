import logging
from .config import Config

config = Config()

class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.handler.setFormatter(self.formatter)

        if not self.logger.handlers:
            self.logger.addHandler(self.handler)

        self.debug_mode = str(config.get.get("DEBUG", "False")).lower() == "true"
        self.logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)

    def debug(self, text: str) -> None:
        self.logger.debug(text,exc_info=self.debug=="true")

    def info(self, text: str) -> None:
        self.logger.info(text)

    def warning(self, text: str) -> None:
        self.logger.warning(text)

    def error(self, text: str) -> None:
        self.logger.error(text,exc_info=self.debug_mode)

    def critical(self, text: str) -> None:
        self.logger.critical(text)

    def exception(self, text: str) -> None:
        """Logs an ERROR message with exception info (stack trace)."""
        self.logger.exception(text)

