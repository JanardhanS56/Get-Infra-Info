import unittest
import math
from garuda.geo import calculate_square_bbox, validate_coordinates, haversine_distance_km


class TestGeospatialEngine(unittest.TestCase):
    def test_coordinate_validation(self):
        valid, _ = validate_coordinates(12.9716, 77.5946)
        self.assertTrue(valid)

        invalid_lat, msg = validate_coordinates(95.0, 77.5946)
        self.assertFalse(invalid_lat)
        self.assertIn("Latitude", msg)

        invalid_lon, msg = validate_coordinates(12.0, 195.0)
        self.assertFalse(invalid_lon)
        self.assertIn("Longitude", msg)

    def test_square_bbox_metrics(self):
        bbox = calculate_square_bbox(12.9716, 77.5946, side_length_km=10.0)
        self.assertEqual(bbox["side_length_km"], 10.0)
        self.assertEqual(bbox["area_sq_km"], 100.0)
        self.assertAlmostEqual(bbox["diagonal_km"], 14.142, places=2)
        self.assertTrue(bbox["south"] < bbox["center_lat"] < bbox["north"])
        self.assertTrue(bbox["west"] < bbox["center_lon"] < bbox["east"])

    def test_haversine_distance(self):
        # North-South distance for ~0.045 degrees should be roughly 5 km
        bbox = calculate_square_bbox(0.0, 0.0, side_length_km=10.0)
        dist_ns = haversine_distance_km(bbox["south"], 0.0, bbox["north"], 0.0)
        self.assertAlmostEqual(dist_ns, 10.0, delta=0.1)

        dist_ew = haversine_distance_km(0.0, bbox["west"], 0.0, bbox["east"])
        self.assertAlmostEqual(dist_ew, 10.0, delta=0.1)


if __name__ == "__main__":
    unittest.main()
