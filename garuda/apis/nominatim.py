from typing import Dict, Any, Optional, List
import requests
from ..models import PlaceInfo

USER_AGENT = "GarudaSpatialIntelligence/1.0 (terminal-app; contact: open-geo@garuda.local)"


def fetch_place_info(lat: float, lon: float, timeout: int = 10) -> PlaceInfo:
    """
    Reverse geocodes coordinates using OpenStreetMap Nominatim.
    Falls back gracefully if the API fails or is rate limited.
    """
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}&zoom=14&addressdetails=1"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            address = data.get("address", {})

            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("municipality")
            )
            suburb = address.get("suburb") or address.get("neighbourhood") or address.get("quarter")
            district = address.get("county") or address.get("district") or address.get("state_district")
            state = address.get("state") or address.get("province")
            country = address.get("country")
            country_code = address.get("country_code", "").upper()
            postcode = address.get("postcode")
            display_name = data.get("display_name", "Unknown Area")

            return PlaceInfo(
                display_name=display_name,
                city=city,
                suburb=suburb,
                district=district,
                state=state,
                country=country,
                country_code=country_code,
                postcode=postcode,
                osm_type=data.get("osm_type"),
            )
    except Exception:
        pass

    # Fallback placeholder if offline or throttled
    return PlaceInfo(
        display_name=f"Coordinate Location ({lat:.4f}, {lon:.4f})",
        city="Unspecified",
        state="Unspecified",
        country="Unspecified",
    )


def search_pois_in_viewbox(
    south: float, west: float, north: float, east: float, query: str, limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Searches for points of interest within the specified bounding box viewbox.
    viewbox format for Nominatim: left,top,right,bottom (i.e. west, north, east, south)
    """
    viewbox = f"{west:.6f},{north:.6f},{east:.6f},{south:.6f}"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=jsonv2&bounded=1&viewbox={viewbox}&limit={limit}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []
