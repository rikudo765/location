import unittest
from app.main.loc_types import Point, PointWithDistance
from app.main.geohash import encode


class TestPoint(unittest.TestCase):
    def test_to_json(self):
        point = Point("id1", 50.45466, 30.5238)
        expected = {
            "point_id": "id1", "latitude": 50.45466, "longitude": 30.5238, "geohash": encode(50.45466, 30.5238)
        }
        self.assertEqual(point.to_json(), expected)

    def test_from_json(self):
        json = {"point_id": "id", "latitude": 50.45466, "longitude": 30.5238, "geohash": str(encode(50.45466, 30.5238))}
        expected = Point("id", 50.45466, 30.5238)
        self.assertEqual(Point.from_json(json), expected)


class TestPointWithDistance(unittest.TestCase):
    def test_to_json(self):
        point = PointWithDistance(Point("id1", 50.45466, 30.5238), 10)
        expected = {
            "point_id": "id1",
            "latitude": 50.45466,
            "longitude": 30.5238,
            "geohash": encode(50.45466, 30.5238),
            "distance": 10
        }
        self.assertEqual(point.to_json(), expected)


if __name__ == '__main__':
    unittest.main()
