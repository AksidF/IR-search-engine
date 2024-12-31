import logging


class CustomFormatter(logging.Formatter):
    """
    CustomFormatter class that used to custom date format.
    """

    log_format = "[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s"

    def __init__(self):
        super().__init__(self.log_format, datefmt="%Y-%m-%d %H:%M:%S")


class Logger:
    """
    Logger class that used to log the process.
    """

    def __init__(self, level=logging.INFO):
        # Create a root logger and clear existing handlers
        self.logger = logging.getLogger()
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Set up the custom handler with the formatter
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())

        # Configure root logger
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

    def get_logger(self):
        """Returns the configured logger instance."""
        return self.logger