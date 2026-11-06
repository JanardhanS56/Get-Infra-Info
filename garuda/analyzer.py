from typing import Tuple
from .models import (
    AreaAnalysisReport,
    BoundingBox,
    PlaceInfo,
    BuildingStats,
    RoadStats,
    CriticalInfrastructure,
    CivicAndEnvironment,
)


def compute_urbanization_index(building_density: float, road_density: float) -> Tuple[str, str]:
    """
    Determines urbanization classification and detailed summary.
    """
    if building_density >= 1200 or road_density >= 300:
        return (
            "Hyper-Dense Urban Metropolitan",
            "Extremely high concentration of built structures and deeply interconnected multi-tier road network.",
        )
    elif building_density >= 450 or road_density >= 120:
        return (
            "Developed Urban Center",
            "High structural density with established grid, primary transit corridors, and active commercial hubs.",
        )
    elif building_density >= 100 or road_density >= 40:
        return (
            "Suburban / Developing Town",
            "Moderate building footprint with expanding residential layouts and evolving arterial connectivity.",
        )
    elif building_density >= 15 or road_density >= 8:
        return (
            "Semi-Rural / Outskirts",
            "Low-density settlements interspersed with agricultural, industrial, or natural terrain.",
        )
    else:
        return (
            "Rural / Wilderness / Open Terrain",
            "Sparse built presence characterized by natural terrain, water bodies, or unpaved tracks.",
        )


def compute_infrastructure_score(
    critical: CriticalInfrastructure,
    civic: CivicAndEnvironment,
    roads: RoadStats,
    area_sq_km: float = 100.0,
) -> Tuple[str, int]:
    """
    Scores infrastructure coverage on a scale of 0 to 100 based on presence
    of emergency services, healthcare, education, financial access, and mobility.
    """
    score = 0

    # Healthcare (up to 25 pts)
    if critical.hospitals >= 5:
        score += 20
    elif critical.hospitals >= 1:
        score += 12
    if critical.clinics + critical.pharmacies >= 10:
        score += 5
    elif critical.clinics + critical.pharmacies >= 2:
        score += 3

    # Emergency & Safety (up to 20 pts)
    if critical.police_stations >= 2:
        score += 10
    elif critical.police_stations >= 1:
        score += 6
    if critical.fire_stations >= 1:
        score += 10
    elif critical.police_stations >= 1:
        score += 2

    # Education (up to 20 pts)
    if critical.schools >= 15:
        score += 12
    elif critical.schools >= 3:
        score += 7
    if critical.colleges_universities >= 2:
        score += 8
    elif critical.colleges_universities >= 1:
        score += 5

    # Mobility & Roads (up to 20 pts)
    if roads.motorway_trunk + roads.primary_secondary >= 15:
        score += 12
    elif roads.motorway_trunk + roads.primary_secondary >= 3:
        score += 7
    if roads.railways >= 1:
        score += 4
    if roads.pedestrian_cycleways >= 10:
        score += 4

    # Civic & Utilities (up to 15 pts)
    if civic.banks_and_atms >= 10:
        score += 8
    elif civic.banks_and_atms >= 2:
        score += 4
    if civic.fuel_charging_stations >= 4:
        score += 4
    if civic.supermarkets_markets >= 4:
        score += 3

    score = min(100, max(0, score))

    if score >= 80:
        rating = f"Tier-1 Critical Infrastructure ({score}/100) - Comprehensive Civic & Emergency Coverage"
    elif score >= 55:
        rating = f"Tier-2 Established Infrastructure ({score}/100) - Strong Regional & Commercial Provisioning"
    elif score >= 30:
        rating = f"Tier-3 Developing Infrastructure ({score}/100) - Basic Services with Gaps in Specialized Coverage"
    else:
        rating = f"Tier-4 Limited Infrastructure ({score}/100) - Rural or Low-Access Zone"

    return rating, score
