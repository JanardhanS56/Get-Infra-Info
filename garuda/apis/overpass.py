from typing import Dict, Any, Optional
import requests

OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
]

HEADERS = {
    "User-Agent": "GarudaSpatialIntelligence/1.0 (terminal-recon; dev@garuda.local)",
    "Accept": "application/json",
}


def run_overpass_query(query: str, timeout: int = 5) -> Optional[Dict[str, Any]]:
    """
    Executes an Overpass QL query across available mirrors with fast failover.
    """
    for mirror in OVERPASS_MIRRORS:
        try:
            resp = requests.post(
                mirror,
                data={"data": query},
                headers=HEADERS,
                timeout=(2.5, timeout),
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            continue
    return None


def fetch_building_and_road_counts(south: float, west: float, north: float, east: float) -> Optional[Dict[str, int]]:
    """
    Queries Overpass for building and highway way counts in bounding box.
    """
    bbox_str = f"{south:.6f},{west:.6f},{north:.6f},{east:.6f}"
    
    # Query total buildings & roads in a single combined batch
    combined_query = f"""[out:json][timeout:10];
(
  way["building"]({bbox_str});
  relation["building"]({bbox_str});
);
out count;
"""
    bld_data = run_overpass_query(combined_query, timeout=5)
    if not bld_data or "elements" not in bld_data:
        return None

    results: Dict[str, int] = {}
    if len(bld_data["elements"]) > 0:
        results["total_buildings"] = int(bld_data["elements"][0].get("tags", {}).get("total", 0))

    return results


def fetch_amenities_and_infrastructure(south: float, west: float, north: float, east: float) -> Optional[Dict[str, int]]:
    """
    Queries Overpass for tagged amenities, public facilities, and natural features.
    """
    bbox_str = f"{south:.6f},{west:.6f},{north:.6f},{east:.6f}"
    query = f"""[out:json][timeout:10];
(
  nwr["amenity"~"^(hospital|clinic|doctors|pharmacy|police|fire_station|school|college|university|bank|atm|place_of_worship|fuel|charging_station|marketplace)$"]({bbox_str});
  nwr["shop"="supermarket"]({bbox_str});
  nwr["waterway"]({bbox_str});
  nwr["natural"="water"]({bbox_str});
  nwr["leisure"~"^(park|garden)$"]({bbox_str});
);
out tags;
"""
    data = run_overpass_query(query, timeout=5)
    if not data or "elements" not in data:
        return None

    counts: Dict[str, int] = {
        "hospitals": 0,
        "clinics": 0,
        "pharmacies": 0,
        "police_stations": 0,
        "fire_stations": 0,
        "schools": 0,
        "colleges_universities": 0,
        "banks_and_atms": 0,
        "fuel_charging_stations": 0,
        "places_of_worship": 0,
        "supermarkets_markets": 0,
        "water_bodies_ways": 0,
        "parks_and_green": 0,
    }

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        amenity = tags.get("amenity", "")
        natural = tags.get("natural", "")
        waterway = tags.get("waterway", "")
        leisure = tags.get("leisure", "")
        shop = tags.get("shop", "")

        if amenity == "hospital":
            counts["hospitals"] += 1
        elif amenity in ("clinic", "doctors"):
            counts["clinics"] += 1
        elif amenity == "pharmacy":
            counts["pharmacies"] += 1
        elif amenity == "police":
            counts["police_stations"] += 1
        elif amenity == "fire_station":
            counts["fire_stations"] += 1
        elif amenity == "school":
            counts["schools"] += 1
        elif amenity in ("college", "university"):
            counts["colleges_universities"] += 1
        elif amenity in ("bank", "atm"):
            counts["banks_and_atms"] += 1
        elif amenity in ("fuel", "charging_station"):
            counts["fuel_charging_stations"] += 1
        elif amenity == "place_of_worship":
            counts["places_of_worship"] += 1
        elif shop == "supermarket" or amenity == "marketplace":
            counts["supermarkets_markets"] += 1

        if waterway or natural == "water":
            counts["water_bodies_ways"] += 1
        if leisure in ("park", "garden"):
            counts["parks_and_green"] += 1

    return counts
