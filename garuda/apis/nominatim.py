from typing import Dict, Any, Optional
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
