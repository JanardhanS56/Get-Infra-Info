from typing import Dict, Any, Tuple, Optional
import requests

WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def fetch_elevation_and_weather(lat: float, lon: float, timeout: int = 8) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Fetches elevation (meters above sea level) and current weather conditions
    from the Open-Meteo public API.
    
    Returns:
        (elevation_m, temperature_c, weather_description)
    """
    elevation_m = None
    temperature_c = None
    weather_desc = None

    # Fetch elevation
    try:
        elev_url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
        r = requests.get(elev_url, timeout=timeout)
        if r.status_code == 200:
            elevations = r.json().get("elevation", [])
            if elevations:
                elevation_m = round(float(elevations[0]), 1)
    except Exception:
        pass

    # Fetch weather
    try:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
        r = requests.get(weather_url, timeout=timeout)
        if r.status_code == 200:
            current = r.json().get("current", {})
            temperature_c = current.get("temperature_2m")
            wcode = current.get("weather_code")
            weather_desc = WEATHER_CODE_MAP.get(wcode, "Unknown conditions")
    except Exception:
        pass

    return elevation_m, temperature_c, weather_desc
