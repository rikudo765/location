import unittest
import uuid
import os
from app.main import create_app
from app.main.geohash import encode


class TestService(unittest.TestCase):

    def setUp(self):
        os.environ["TEST_MODE"] = "1"

    def test_point_lifecycle(self):
        point = {
            "point_id": "test-location-lifecycle-" + str(uuid.uuid4()),
            "latitude": 50.45466,
            "longitude": 30.5238,
            "geohash": encode(50.45466, 30.5238)
        }

        with create_app().test_client() as client:
            resp = client.post('/location/v1/points', json=point)
            self.assertEqual(resp.status_code, 201)  # created new point

            resp = client.get('/location/v1/points/{0}'.format(point["point_id"]))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, point)

            resp = client.post('/location/v1/points', json=point)
            self.assertEqual(resp.status_code, 200)  # updated existing event

            resp = client.delete('/location/v1/points/{0}'.format(point["point_id"]))
            self.assertEqual(resp.status_code, 200)

            resp = client.get('/location/v1/points/{0}'.format(point["point_id"]))
            self.assertEqual(resp.status_code, 404)

            resp = client.delete('/location/v1/points/{0}'.format(point["point_id"]))
            self.assertEqual(resp.status_code, 404)

    def test_searcher_at_circle(self):
        pt1 = {
            "point_id": "test-location-search-" + str(uuid.uuid4()),
            "latitude": 80.25710998046067,
            "longitude": 20.181884765625
        }

        pt2 = {
            "point_id": "test-location-search-" + str(uuid.uuid4()),
            "latitude": 79.97041699075265,
            "longitude": 21.214599609375
        }
        with create_app().test_client() as client:
            client.post('/location/v1/points', json=pt1)
            client.post('/location/v1/points', json=pt2)

            query = "longitude={0}&latitude={1}&radius={2}".format(20.709228515625, 80.11243456832592, 20000)
            resp = client.get('/location/v1/search?' + query)
            self.assertEqual(resp.status_code, 200)

        points = resp.json["points"]
        ids = [p["point_id"] for p in points]
        self.assertTrue((pt1["point_id"] in ids) and (pt2["point_id"] in ids))
        for p in points:
            if p["point_id"] == pt1["point_id"]:
                self.assertTrue(18930 <= p["distance"] <= 18950)
            elif p["point_id"] == pt2["point_id"]:
                self.assertTrue(18530 <= p["distance"] <= 18550)
        client.delete('/location/v1/points/{0}'.format(pt1["point_id"]))
        client.delete('/location/v1/points/{0}'.format(pt2["point_id"]))

    def test_searcher_at_rectangle(self):
        point_1 = {
            "point_id": "test-location-search-1" + str(uuid.uuid4()),
            "latitude": -22.024545601240337,
            "longitude": 138.36181640625123
        }  # NOT in rectangle

        point_2 = {
            "point_id": "test-location-search-1" + str(uuid.uuid4()),
            "latitude": -20.704738720055513,
            "longitude": 135.67016601562512
        }  # in rectangle
        point_3 = {
            "point_id": "test-location-search-1" + str(uuid.uuid4()),
            "latitude": -22.156883186860703,
            "longitude": 136.93359375123412
        }  # in rectangle
        with create_app().test_client() as client:
            client.post('/location/v1/points', json=point_1)
            client.post('/location/v1/points', json=point_2)
            client.post('/location/v1/points', json=point_3)

            query = "top_left_long={0}&top_left_lat={1}&bottom_right_long={2}&bottom_right_lat={3}&" \
                    "current_long={4}&current_lat={5}".format(135.054931640625, -20.550508894195637,
                                                              137.504882812512, -22.299261499741213,
                                                              137.548828125213, -20.529933125170764)
            resp = client.get('/location/v1/search2?' + query)
            self.assertEqual(resp.status_code, 200)

        points = resp.json["points"]
        ids = [p["point_id"] for p in points]

        self.assertTrue((point_1["point_id"] not in ids) and
                        (point_2["point_id"] in ids) and
                        (point_2["point_id"] in ids))

        for p in points:
            if p["point_id"] == point_2["point_id"]:
                self.assertTrue(196430 <= p["distance"] <= 196550)
            elif p["point_id"] == point_3["point_id"]:
                self.assertTrue(191750 <= p["distance"] <= 191870)

        client.delete('/location/v1/points/{0}'.format(point_1["point_id"]))
        client.delete('/location/v1/points/{0}'.format(point_2["point_id"]))
        client.delete('/location/v1/points/{0}'.format(point_3["point_id"]))

    def test_error_point_not_found(self):
        with create_app().test_client() as client:
            resp = client.get('/location/v1/points/some-unknown-point-123')
            expected = {
                "code": 404,
                "name": "Not Found",
                "description": "Point some-unknown-point-123 not found"
            }
            self.assertEqual(resp.json, expected)

    def test_error_point_no_latitude(self):
        pt1 = {
            "point_id": "some-id", "longitude": 23.4562
        }
        with create_app().test_client() as client:
            resp = client.post('/location/v1/points', json=pt1)
            expected = {
                "code": 400,
                "name": "Bad Request",
                "description": "Invalid json: Key error : 'latitude'"
            }
            self.assertEqual(resp.json, expected)

    def test_error_point_no_longitude(self):
        req = {
            "point_id": "some-point-id", "latitude": 26.2354
        }
        with create_app().test_client() as client:
            resp = client.post('/location/v1/points', json=req)
            expected = {
                "code": 400,
                "name": "Bad Request",
                "description": "Invalid json: Key error : 'longitude'"
            }
            self.assertEqual(resp.json, expected)

    def test_error_invalid_url(self):
        with create_app().test_client() as client:
            resp = client.get('/location/v1/points-')
            expected = {
                "code": 404,
                "name": "Not Found",
                "description": "The requested URL was not found on the server."
                               " If you entered the URL manually please check your spelling and try again."
            }
            self.assertEqual(resp.json, expected)


if __name__ == '__main__':
    unittest.main()
