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
        self._logger.level("Time", no=42, icon="⌛", color="<magenta>")

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

    def timeit(self, function: Callable) -> Callable:
        """
        Decorator to measure and log the execution time of a function.

        Args:
            function: The function to time.

        Returns:
            The wrapper function that logs execution time.
        """

        def wrapper(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
            self._logger.info(f"Entering function {function.__name__}.")
            start_time = time()
            result = function(*args, **kwargs)
            end_time = time()
            elapsed_time = end_time - start_time
            self._logger.log(
                "Time", f"Function {function.__name__} ran for {elapsed_time:.4f} seconds."
            )
            self._logger.info(f"Exiting function {function.__name__}.")
            return result

        return wrapper

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
        if not data:
            self._logger.info("Table of Results:\n(No data provided)")
            return

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

        self._logger.info("Table of Results:\n{}", table)


logger = LoguruPro()
