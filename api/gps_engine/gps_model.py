from schema import Schema, Optional, Or
import pandas as pd
from uuid import uuid4
from pathlib import Path
import pickle
from gps_engine.base import BaseModel

METHODS = ["filter", "smooth", "both", "none"]
OUTPUT = ["distance", "path", "both"]


class GpsModel(BaseModel):
    def __init__(self, data):
        super().__init__(data=data)

    @classmethod
    def schema(cls):
        return Schema(
            {
                "longitude": [float],
                "latitude": [float],
                Optional("model_id"): str,
                Optional("method"): Or(*METHODS),
                Optional("output"): Or(*OUTPUT),
                Optional("distance_cutoff"): float,
                Optional("smoothing_factor"): float,
            }
        )

    @property
    def lon(self):
        return self._data["longitude"]

    @property
    def lat(self):
        return self._data["latitude"]

    @property
    def method(self):
        return self._data.get("method", "both")

    @property
    def output(self):
        return self._data.get("output", "both")

    @property
    def distance_cutoff(self):
        return self._data.get("distance_cutoff", 1000)

    @property
    def smoothing_factor(self):
        return self._data.get("smoothing_factor", 0.1)

    @property
    def path(self):
        return pd.DataFrame({"longitude": self.lon, "latitude": self.lat})

    @property
    def model_id(self):
        if "model_id" not in self._data.keys():
            self._data["model_id"] = str(uuid4())[:5]
        return self._data["model_id"]

    def save(self):
        with open(
            f"{Path(__file__).resolve().parents[1]}/history/{self.model_id}.pickle",
            "wb",
        ) as file:
            pickle.dump(self, file)

    @staticmethod
    def load(model_id):
        with open(
            f"{Path(__file__).resolve().parents[1]}/history/{model_id}.pickle", "rb"
        ) as file:
            return pickle.load(file)
