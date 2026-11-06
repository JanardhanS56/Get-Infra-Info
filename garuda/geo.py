import math
from typing import Tuple, Dict, Any

EARTH_RADIUS_KM = 6371.0088


def validate_coordinates(lat: float, lon: float) -> Tuple[bool, str]:
    """Validate latitude and longitude ranges."""
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False, "Coordinates must be numbers."
    if lat < -90.0 or lat > 90.0:
        return False, f"Latitude {lat} is out of bounds (-90.0 to 90.0)."
    if lon < -180.0 or lon > 180.0:
        return False, f"Longitude {lon} is out of bounds (-180.0 to 180.0)."
    return True, "Valid"


def calculate_square_bbox(
    center_lat: float,
    center_lon: float,
    side_length_km: float = 10.0,
) -> Dict[str, Any]:
    """
    Calculates a square bounding box centered at (center_lat, center_lon)
    with edge length `side_length_km` (default 10 km x 10 km = 100 sq km).
    
    Returns:
        dict containing south, west, north, east, and dimension metrics.
    """
    valid, msg = validate_coordinates(center_lat, center_lon)
    if not valid:
        raise ValueError(msg)

    half_side = side_length_km / 2.0  # 5 km in each direction

    # Delta latitude in degrees
    d_lat_deg = (half_side / EARTH_RADIUS_KM) * (180.0 / math.pi)
    south = max(-90.0, center_lat - d_lat_deg)
    north = min(90.0, center_lat + d_lat_deg)

    # Delta longitude at center latitude
    lat_rad = math.radians(center_lat)
    cos_lat = math.cos(lat_rad)
    if abs(cos_lat) < 1e-6:
        d_lon_deg = 180.0
    else:
        d_lon_deg = (half_side / (EARTH_RADIUS_KM * cos_lat)) * (180.0 / math.pi)

    west = center_lon - d_lon_deg
    east = center_lon + d_lon_deg

    # Longitude normalization to [-180, 180]
    if west < -180.0:
        west += 360.0
    if east > 180.0:
        east -= 360.0

    return {
        "center_lat": round(center_lat, 6),
        "center_lon": round(center_lon, 6),
        "south": round(south, 6),
        "west": round(west, 6),
        "north": round(north, 6),
        "east": round(east, 6),
        "side_length_km": side_length_km,
        "area_sq_km": round(side_length_km * side_length_km, 2),
        "diagonal_km": round(math.sqrt(2 * (side_length_km ** 2)), 3),
        # Overpass bbox format is (south, west, north, east)
        "overpass_bbox": f"{round(south, 6)},{round(west, 6)},{round(north, 6)},{round(east, 6)}",
    }


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points in km."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_KM * c
