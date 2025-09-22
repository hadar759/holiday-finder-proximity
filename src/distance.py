from math import radians, cos, sin, asin, sqrt
from typing import Tuple
import geocoder


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Returns distance in meters
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Earth radius in meters
    r = 6371000
    return c * r


def geocode_address(address: str) -> Tuple[float, float]:
    """
    Convert an address to latitude/longitude using geocoder
    Returns (latitude, longitude)
    """
    try:
        headers = {"User-Agent": "holiday-finder/1.0 (geocoding application)"}
        g = geocoder.osm(address, headers=headers)

        if not g.ok:
            raise ValueError(f"Address not found: {address}")

        return float(g.lat), float(g.lng)

    except Exception as e:
        raise Exception(f"Failed to geocode address '{address}': {e}")
