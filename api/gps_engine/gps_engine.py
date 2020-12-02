from gps_engine.gps_model import GpsModel
from gps_engine.utils.utils import (
    hard_filter,
    kalman_smoothing,
    total_distance,
    plotter,
)


class GpsEngine(GpsModel):
    def __init__(self, data):
        self.output_path = None
        super().__init__(data)

    def compute_path(self):
        if self.method == "both":
            self.output_path = kalman_smoothing(
                hard_filter(self.path, distance_cutoff=self.distance_cutoff),
                smoothing_factor=self.smoothing_factor,
            )
        if self.method == "filter":
            self.output_path = hard_filter(
                self.path, distance_cutoff=self.distance_cutoff
            )
        if self.method == "smooth":
            self.output_path = kalman_smoothing(
                self.path, smoothing_factor=self.smoothing_factor
            )

    def compute_output(self):
        self.compute_path()
        path = {
            "latitude": list(self.output_path["latitude"]),
            "longitude": list(self.output_path["longitude"]),
        }
        if self.output == "path":
            return {"model_id": self.model_id, "path": path}
        if self.output == "distance":
            return {
                "model_id": self.model_id,
                "distance": total_distance(self.output_path),
            }
        if self.output == "both":
            return {
                "model_id": self.model_id,
                "path": path,
                "distance": total_distance(self.output_path),
            }

    def plot_map(self):
        return plotter(self)
