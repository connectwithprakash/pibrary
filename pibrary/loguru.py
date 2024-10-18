from time import time
from typing import Any, Callable, Dict, List, Tuple, Optional
from loguru import logger as loguru_logger


class LoguruPro:
    def __init__(self):
        self._logger = loguru_logger
        self._setup_custom_levels()

    def _setup_custom_levels(self) -> None:
        """
        Set up custom log levels.
        """
        # Custom log levels
        self._logger.level("TIME", no=15, icon="⌛", color="<magenta>")
        self._logger.level("DATA", no=100, icon="📦", color="<cyan>")

    def __getattr__(self, name: str) -> Callable:
        """
        Delegate attribute access to the wrapped Loguru logger object.
        Allows access to all Loguru logger methods.

        Args:
            name: The attribute or method name.

        Returns:
            The attribute or method from the Loguru logger.
        """
        return getattr(self._logger, name)

    def time(self, message: str) -> None:
        """
        Log a message at the custom TIME level.

        Args:
            message: The message to log.
        """
        self._logger.log("TIME", message)

    def data(self, message: str) -> None:
        """
        Log a message at the custom DATA level.

        Args:
            message: The message to log.
        """
        self._logger.log("DATA", message)

    def timeit(self, function: Optional[Callable] = None):
        """
        Decorator or context manager to measure and log the execution time of a function or code block.

        Args:
            function: The function to time (if used as a decorator).

        Returns:
            The wrapper function that logs execution time (if used as a decorator),
            or the context manager (if used with a with statement).
        """
        if function is not None:
            # Used as a decorator
            def wrapper(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
                self._logger.trace(f"Entering function {function.__name__}.")
                start_time = time()
                result = function(*args, **kwargs)
                end_time = time()
                elapsed_time = end_time - start_time
                self._logger.log("TIME", f"Function {function.__name__} ran for {elapsed_time:.4f} seconds.")
                self._logger.trace(f"Exiting function {function.__name__}.")
                return result

            return wrapper
        else:
            # Used as a context manager
            class TimerContextManager:
                def __init__(self, logger_instance):
                    self.logger_instance = logger_instance

                def __enter__(self):
                    self.start_time = time()
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    end_time = time()
                    elapsed_time = end_time - self.start_time
                    self.logger_instance.log("TIME", f"Code block ran for {elapsed_time:.4f} seconds.")

            return TimerContextManager(self)

    def log_table(
        self,
        data: List[List[str]],
        headers: List[str] = None,
        alignments: List[str] = None,
        row_separator: str = "-+-",
        column_separator: str = " | ",
    ) -> None:
        """
        Logs a given list of data as a formatted table.

        Args:
            data: List of rows, where each row is a list of values.
            headers: Optional headers for the table columns.
            alignments: Optional list of alignments for each column ("left", "center", "right").
            row_separator: Custom separator string for rows.
            column_separator: Custom separator string for columns.
        """
        # If headers are not provided, create default headers
        num_columns = max(len(row) for row in data)
        headers = headers or [f"Column {i+1}" for i in range(num_columns)]

        # Ensure the headers match the number of columns
        if len(headers) < num_columns:
            headers.extend([f"Column {i+1}" for i in range(len(headers), num_columns)])

        # Ensure alignments match the number of columns, or default to 'left'
        if alignments is None:
            alignments = ["left"] * num_columns
        else:
            alignments = (alignments + ["left"] * num_columns)[:num_columns]

        # Calculate column widths based on the maximum length of data in each column
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]

        def format_cell(value: str, width: int, alignment: str) -> str:
            if alignment == "left":
                return f"{value:<{width}}"
            elif alignment == "center":
                return f"{value:^{width}}"
            elif alignment == "right":
                return f"{value:>{width}}"
            return value

        def format_row(row: List[str], is_header: bool = False) -> str:
            return column_separator.join(
                format_cell(str(item), col_widths[i], alignments[i]) for i, item in enumerate(row)
            )

        separator_row = row_separator.join("-" * width for width in col_widths)

        table = "\n".join(
            [
                format_row(headers, is_header=True),
                separator_row,
                "\n".join(format_row(row) for row in data),
            ]
        )

        self._logger.log("DATA", f"Table of Results:\n{table}")


logger = LoguruPro()
