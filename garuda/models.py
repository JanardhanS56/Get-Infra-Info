from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    center_lat: float
    center_lon: float
    south: float
    west: float
    north: float
    east: float
    side_length_km: float = 10.0
    area_sq_km: float = 100.0
    diagonal_km: float
    overpass_bbox: str


class PlaceInfo(BaseModel):
    display_name: str = "Unknown Location"
    city: Optional[str] = None
    suburb: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    postcode: Optional[str] = None
    osm_type: Optional[str] = None
    elevation_m: Optional[float] = None
    current_temp_c: Optional[float] = None
    weather_condition: Optional[str] = None


class BuildingStats(BaseModel):
    total_buildings: int = 0
    residential_buildings: int = 0
    commercial_industrial: int = 0
    apartments: int = 0
    other_buildings: int = 0
    building_density_per_sq_km: float = 0.0


class RoadStats(BaseModel):
    total_road_segments: int = 0
    motorway_trunk: int = 0
    primary_secondary: int = 0
    tertiary_residential: int = 0
    service_living_street: int = 0
    track_unclassified: int = 0
    pedestrian_cycleways: int = 0
    bridges: int = 0
    tunnels: int = 0
    railways: int = 0
    road_density_per_sq_km: float = 0.0


class CriticalInfrastructure(BaseModel):
    hospitals: int = 0
    clinics: int = 0
    pharmacies: int = 0
    police_stations: int = 0
    fire_stations: int = 0
    schools: int = 0
    colleges_universities: int = 0
    emergency_services_total: int = 0
    healthcare_total: int = 0
    education_total: int = 0


class CivicAndEnvironment(BaseModel):
    places_of_worship: int = 0
    banks_and_atms: int = 0
    fuel_charging_stations: int = 0
    water_bodies_ways: int = 0
    parks_and_green: int = 0
    supermarkets_markets: int = 0


class AreaAnalysisReport(BaseModel):
    bbox: BoundingBox
    place: PlaceInfo
    buildings: BuildingStats
    roads: RoadStats
    critical_infra: CriticalInfrastructure
    civic_env: CivicAndEnvironment
    urbanization_index: str
    infrastructure_score: str
    analysis_timestamp: str
