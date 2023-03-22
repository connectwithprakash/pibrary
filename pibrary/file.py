from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

import joblib
import pandas as pd
import torch
from loguru import logger


class File:
    """
    Class to read and write files.
    """

    def __init__(self, path: str, *args, **kwargs) -> None:
        """
        Creates an instance of File with specified file path.

        Args:
            path: Path of the file for read/write.

        """
        self._mode = "r"
        self._path = path
        self._obj_file = None

    def read(self) -> File:
        """
        Sets the io mode to read, and path variable to read from.

        Returns: Class object to chain with other methods.

        """
        self._mode = "r"
        return self

    def write(self, obj_file: Any) -> File:
        """
        Sets the io mode to write, and path variable to write to.

        Args:
            obj_file: Object to save like dict for j

        Returns: Class object to chain with other methods.

        """
        self._mode = "w"
        self._obj_file = obj_file
        return self

    def json(self, **kwargs) -> Optional[Dict[str, List[str]]]:
        """
        Reads or writes json file according to mode set by read/write method.

        Args:
            **kwargs: Keyword arguments for diff read/write like. Eg:nt=4 for json read.

        Returns: obj_file if read mode else nothing is returned.

        """
        try:
            if (self._mode == "w") and (self._obj_file is not None):
                json.dump(self._obj_file, open(self._path, "w"), **kwargs)
                logger.success(f"File written at {self._path}")
            elif self._mode == "r":
                self._obj_file = json.load(open(self._path, "r"))
                logger.success(f"File read from {self._path}")
                return self._obj_file
        except:
            if self._mode == "w":
                logger.exception(f"Cannot write file at {self._path}")
            else:
                logger.exception(f"Cannot read file from {self._path}")
            logger.critical("Terminating the process.")
            sys.exit()

    def pickle(self):
        """
        Reads or writes pickle file according to mode set by read/write method.

        Returns: obj_file if read mode else nothing is returned.

        """
        try:
            if (self._mode == "w") and (self._obj_file is not None):
                joblib.dump(self._obj_file, self._path)
                logger.success(f"File written at {self._path}")
            elif self._mode == "r":
                self._obj_file = joblib.load(self._path)
                logger.success(f"File read from {self._path}")
                return self._obj_file
        except:
            if self._mode == "w":
                logger.exception(f"Cannot write file at {self._path}")
            else:
                logger.exception(f"Cannot read file from {self._path}")
            logger.critical("Terminating the process.")
            sys.exit()

    def csv(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Reads or writes csv file according to mode set by read/write method.

        Returns: Dataframe if read mode else nothing is returned.

        """
        try:
            if (self._mode == "w") and (self._obj_file is not None):
                self._obj_file.to_csv(self._path, index=False, **kwargs)
                logger.success(f"File written at {self._path}")
            elif self._mode == "r":
                self._obj_file = pd.read_csv(self._path, **kwargs)
                logger.success(f"File read from {self._path}")
                return self._obj_file
        except:
            if self._mode == "w":
                logger.exception(f"Cannot write file at {self._path}")
            else:
                logger.exception(f"Cannot read file from {self._path}")
            logger.critical("Terminating the process.")
            sys.exit()

    def torch(self, **kwargs):
        """
        Reads or writes torch file according to mode set by read/write method.

        Args:
            **kwargs: Keyword arguments for file read/write. Eg: cuda_device_num = 0 to read of cuda:0.

        Returns: torch object if read mode else nothing is returned.

        """
        try:
            if (self._mode == "w") and (self._obj_file is not None):
                torch.save(self._obj_file, self._path)
                logger.success(f"File written at {self._path}")
            elif self._mode == "r":
                cuda_device_num = kwargs.get("cuda_device_num")
                device = torch.device(
                    f"cuda:{cuda_device_num}" if torch.cuda.is_available(
                    ) and cuda_device_num is not None else "cpu"
                )
                self._obj_file = torch.load(self._path, map_location=device)
                logger.success(f"File read from {self._path}")
                return self._obj_file
        except:
            if self._mode == "w":
                logger.exception(f"Cannot write file at {self._path}")
            else:
                logger.exception(f"Cannot read file from {self._path}")
            logger.critical("Terminating the process.")
            sys.exit()