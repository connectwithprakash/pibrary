# Test cases for the file module

import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, List

import pandas as pd
import joblib
from pytest import fixture

from pibrary.file import File


class TestFile:

    @fixture
    def json_data(self) -> Dict[str, List[str]]:
        return {"colors": ["red", "blue", "green"]}

    @fixture
    def json_file(self, json_data) -> Path:
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(json_data, f)
            return Path(f.name)

    @fixture
    def csv_data(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "name": ["Alice", "Bob", "Charlie"],
                "age": [25, 30, 35],
                "city": ["New York", "Paris", "Tokyo"],
            }
        )

    @fixture
    def csv_file(self, csv_data) -> Path:
        with NamedTemporaryFile(mode="w", delete=False) as f:
            csv_data.to_csv(f, index=False)
            return Path(f.name)

    @fixture
    def pickle_data(self) -> List[str]:
        return ["foo", "bar", "baz"]

    @fixture
    def pickle_file(self, pickle_data) -> Path:
        with NamedTemporaryFile(mode="wb", delete=False) as f:
            joblib.dump(pickle_data, f)
            return Path(f.name)

    def test_json_read(self, json_file, json_data):
        obj_file = File(json_file).read().json()
        assert obj_file == json_data

    def test_csv_read(self, csv_file, csv_data):
        obj_file = File(csv_file).read().csv()
        assert obj_file.equals(csv_data)
    
    def test_pickle_read(self, pickle_file, pickle_data):
        obj_file = File(pickle_file).read().pickle()
        assert obj_file == pickle_data

    def test_json_write(self, json_file, json_data):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            File(f.name).write(json_data).json()
            obj_file = json.load(open(f.name, "r"))
            assert obj_file == json_data
    
    def test_csv_write(self, csv_file, csv_data):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            File(f.name).write(csv_data).csv()
            obj_file = pd.read_csv(f.name)
            assert obj_file.equals(csv_data)
    
    def test_pickle_write(self, pickle_file, pickle_data):
        with NamedTemporaryFile(mode="wb", delete=False) as f:
            File(f.name).write(pickle_data).pickle()
            obj_file = joblib.load(f.name)
            assert obj_file == pickle_data
