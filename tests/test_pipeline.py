import unittest
from garuda.models import (
    BoundingBox,
    PlaceInfo,
    BuildingStats,
    RoadStats,
    CriticalInfrastructure,
    CivicAndEnvironment,
    AreaAnalysisReport,
)
from garuda.analyzer import compute_urbanization_index, compute_infrastructure_score


class TestPipelineAndAnalysis(unittest.TestCase):
    def test_urbanization_index_calculation(self):
        # Hyper dense
        rating, desc = compute_urbanization_index(1500.0, 350.0)
        self.assertIn("Hyper-Dense", rating)

        # Rural
        rural_rating, _ = compute_urbanization_index(5.0, 2.0)
        self.assertIn("Rural", rural_rating)

    def test_infrastructure_scoring(self):
        crit = CriticalInfrastructure(
            hospitals=6,
            clinics=12,
            pharmacies=20,
            police_stations=3,
            fire_stations=2,
            schools=20,
            colleges_universities=4,
            emergency_services_total=5,
            healthcare_total=38,
            education_total=24,
        )
        civic = CivicAndEnvironment(
            places_of_worship=15,
            banks_and_atms=15,
            fuel_charging_stations=8,
            water_bodies_ways=5,
            parks_and_green=8,
            supermarkets_markets=10,
        )
        roads = RoadStats(
            total_road_segments=4000,
            motorway_trunk=150,
            primary_secondary=500,
            tertiary_residential=2500,
            service_living_street=600,
            track_unclassified=250,
            pedestrian_cycleways=300,
            bridges=25,
            tunnels=4,
            railways=10,
            road_density_per_sq_km=40.0,
        )
        rating, score = compute_infrastructure_score(crit, civic, roads, area_sq_km=100.0)
        self.assertGreaterEqual(score, 70)
        self.assertIn("Tier-1", rating)


if __name__ == "__main__":
    unittest.main()
