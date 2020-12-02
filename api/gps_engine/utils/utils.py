import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import numpy as np
import plotly.graph_objects as go
from pykalman import KalmanFilter


def haversine_distance(lat1, lon1, lat2, lon2):
    # Function to calculate distance between two pairs of Geo-coordinates using Haversine Approximation
    if not (
        isinstance(lat1, float)
        and isinstance(lon1, float)
        and isinstance(lat2, float)
        and isinstance(lon2, float)
    ):
        return 1e30
    earth_radius = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = earth_radius * c

    return distance * 1000


def kalman_smoothing(gps, smoothing_factor=0.1):
    measurements = np.array([(x, y) for x, y in zip(gps["longitude"], gps["latitude"])])
    initial_state_mean = [measurements[0, 0], 0, measurements[0, 1], 0]

    transition_matrix = [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

    observation_matrix = [[1, 0, 0, 0], [0, 0, 1, 0]]

    kf1 = KalmanFilter(
        transition_matrices=transition_matrix,
        observation_matrices=observation_matrix,
        initial_state_mean=initial_state_mean,
        em_vars=["transition_covariance", "initial_state_covariance"],
    )

    kf1 = kf1.em(measurements, n_iter=5)
    kf1.smooth(measurements)

    kf1 = KalmanFilter(
        transition_matrices=transition_matrix,
        observation_matrices=observation_matrix,
        initial_state_mean=initial_state_mean,
        observation_covariance=smoothing_factor * kf1.observation_covariance,
        em_vars=["transition_covariance", "initial_state_covariance"],
    )

    kf1 = kf1.em(measurements, n_iter=5)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
    return pd.DataFrame(
        {
            "longitude": smoothed_state_means[:, 0],
            "latitude": smoothed_state_means[:, 2],
        }
    )


def hard_filter(gps_path, distance_cutoff=1000):
    distances = []
    gps_clean = gps_path.copy()
    for i in range(len(gps_path) - 1):
        d = haversine_distance(
            gps_path["latitude"][i],
            gps_path["longitude"][i],
            gps_path["latitude"][i + 1],
            gps_path["longitude"][i + 1],
        )
        distances.append(d)
    for i in range(len(gps_path) - 2):
        if distances[i] + distances[i + 1] > distance_cutoff:
            gps_clean = gps_clean.drop(i + 1)
    return gps_clean


def total_distance(gps_path):
    distances = []
    for i in range(len(gps_path) - 1):
        d = haversine_distance(
            gps_path["latitude"][i],
            gps_path["longitude"][i],
            gps_path["latitude"][i + 1],
            gps_path["longitude"][i + 1],
        )
        distances.append(d)
    return float(np.sum(distances))


def plotter(model):
    model.compute_path()
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            mode="markers+lines",
            name="original",
            lon=model.lon,
            lat=model.lat,
            marker={"size": 10},
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            mode="markers+lines",
            name="output",
            lon=model.output_path["longitude"],
            lat=model.output_path["latitude"],
            marker={"size": 10},
        )
    )
    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": np.mean(model.lon), "lat": np.mean(model.lat)},
            "style": "stamen-terrain",
            "center": {"lon": np.mean(model.lon), "lat": np.mean(model.lat)},
            "zoom": 15,
        },
    )
    fig.write_html("./output.html")
