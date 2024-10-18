import inspect
import sys

from time import time
from typing import Any, Callable, Dict, List, Optional, Tuple
from functools import wraps
from loguru import logger as loguru_logger


class TimerContextManager:
    """
    Context manager to measure and log the execution time of code blocks.

    Attributes:
        logger (loguru_logger): Instance of the Loguru logger for logging.
        start_time (float): The time when the context was entered.
    """

    def __init__(self, logger: loguru_logger) -> None:
        """
        Initializes the TimerContextManager with a Loguru logger.

        Args:
            logger (loguru_logger): The logger instance used for logging execution time.
        """
        self.logger = logger

    def __enter__(self) -> "TimerContextManager":
        """Record the start time when entering the context."""
        self.start_time = time()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """Log the elapsed time when exiting the context."""
        elapsed_time = time() - self.start_time
        self.logger.opt(depth=1).log("TIME", f"Code block ran in {elapsed_time:.4f} seconds.")


class LoguruPro:
    """
    Enhanced wrapper for Loguru logger with additional features.

    Methods:
        time(message: str): Log a message at the custom TIME level.
        data(message: str): Log a message at the custom DATA level.
        timeit(function: Optional[Callable] = None): Decorator or context manager for measuring execution time.
        log_table(data: List[List[str]], headers: Optional[List[str]] = None, ...): Log tabular data as a table.
    """

    def __init__(self) -> None:
        """Initialize LoguruPro with custom log levels."""
        self.logger = loguru_logger
        self._setup_custom_levels()

    def _setup_custom_levels(self) -> None:
        """Define custom log levels for TIME and DATA."""
        self.logger.level("TIME", no=15, icon="⏱️", color="<bold><magenta>")
        self.logger.level("DATA", no=100, icon="📊", color="<bold><cyan>")

    def __getattr__(self, name: str) -> Callable:
        """
        Delegate attribute access to the wrapped Loguru logger object.

        Args:
            name (str): The attribute or method name to access.

        Returns:
            Callable: The corresponding attribute or method from the Loguru logger.
        """
        return getattr(self.logger, name)

    def time(self, message: str) -> None:
        """
        Log a message at the custom TIME level.

        Args:
            message (str): The message to log.
        """
        # frame = inspect.currentframe().f_back
        self.logger.opt(depth=1).log("TIME", message)

    def data(self, message: str) -> None:
        """
        Log a message at the custom DATA level.

        Args:
            message (str): The message to log.
        """
        self.logger.opt(depth=1).log("DATA", message)

    def timeit(self, function: Optional[Callable] = None) -> Callable:
        """
        Decorator or context manager for logging execution time.

        Args:
            function (Optional[Callable]): The function to time if used as a decorator.

        Returns:
            Callable: The wrapped function with timing or a context manager.
        """
        if function:

            @wraps(function)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                self.logger.trace(f"Entering {function.__name__}.")
                start_time = time()
                result = function(*args, **kwargs)
                elapsed_time = time() - start_time
                self.logger.opt(depth=1).log("TIME", f"{function.__name__} ran in {elapsed_time:.4f} seconds.")
                self.logger.trace(f"Exiting {function.__name__}.")
                return result

            return wrapper

        return TimerContextManager(self.logger)

    def log_table(
        self,
        data: List[List[str]],
        headers: Optional[List[str]] = None,
        alignments: Optional[List[str]] = None,
        row_separator: str = "-+-",
        column_separator: str = " | ",
    ) -> None:
        """
        Log a list of data as a formatted table.

        Args:
            data (List[List[str]]): The rows of the table, where each row is a list of string values.
            headers (Optional[List[str]]): The headers for the table columns.
            alignments (Optional[List[str]]): Alignment for each column ("left", "center", "right").
            row_separator (str): The string used to separate rows. Default is '-+-'.
            column_separator (str): The string used to separate columns. Default is ' | '.
        """
        num_columns = max(len(row) for row in data)
        headers = headers or [f"Column {i + 1}" for i in range(num_columns)]
        alignments = (alignments or ["left"] * num_columns)[:num_columns]

        # Calculate the maximum width for each column
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]

        def format_cell(value: str, width: int, align: str) -> str:
            """Format a cell based on the specified alignment."""
            align_map = {"left": "<", "center": "^", "right": ">"}
            return f"{value:{align_map.get(align, '<')}{width}}"

        def format_row(row: List[str]) -> str:
            """Format a row with the specified column separator."""
            return column_separator.join(format_cell(item, col_widths[i], alignments[i]) for i, item in enumerate(row))

        separator_row = row_separator.join("-" * width for width in col_widths)
        table = "\n".join([format_row(headers), separator_row] + [format_row(row) for row in data])

        self.logger.log("DATA", f"Table of Results:\n{table}")


# Instantiate the logger
logger = LoguruPro()
