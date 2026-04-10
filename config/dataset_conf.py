"""Dataset validation configuration for open-meteo-HCMC-grid.

This module stores the basic numeric bounds used in EDA and data validation.
The geographic bounds are an approximate outer box for Ho Chi Minh City.
Adjust them if you later replace this with an exact administrative boundary.
"""

DATASET_NAME = "open-meteo-HCMC-grid"

GEO_BOUNDS: dict[str, tuple[float, float]] = {
    "latitude": (10.50, 11.00),
    "longitude": (106.35, 107.00),
}

NUMERIC_BOUNDS: dict[str, tuple[float, float]] = {
    "elevation": (0.0, 1000.0),
    "temperature_2m_mean (Â°C)": (15.0, 45.0),
    "rain_sum (mm)": (0.0, float("inf")),
    "relative_humidity_2m_mean (%)": (0.0, 100.0),
    "surface_pressure_mean (hPa)": (900.0, float("inf")),
    "cloud_cover_mean (%)": (0.0, 100.0),
    "wind_speed_10m_mean (km/h)": (0.0, float("inf")),
}

DEFAULT_COLUMNS = [
    "latitude",
    "longitude",
    "elevation",
    "temperature_2m_mean (Â°C)",
    "rain_sum (mm)",
    "relative_humidity_2m_mean (%)",
    "surface_pressure_mean (hPa)",
    "cloud_cover_mean (%)",
    "wind_speed_10m_mean (km/h)",
]
