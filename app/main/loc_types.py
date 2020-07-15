from app.main import errors
from app.main.geohash import encode


class Point:

    def __init__(self, point_id, latitude, longitude):
        self.point_id = point_id
        self.latitude = latitude
        self.longitude = longitude
        self.geohash = encode(latitude, longitude)

    def to_json(self):
        return {
            "point_id": self.point_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "geohash": self.geohash
        }

    @staticmethod
    def from_json(json):
        try:
            point_id = json["point_id"]
            latitude = float(json["latitude"])
            longitude = float(json["longitude"])
        except ValueError as err:
            raise errors.InvalidJson("Value error : {0}".format(err))
        except KeyError as err:
            raise errors.InvalidJson("Key error : {0}".format(err))

        return Point(point_id, latitude, longitude)

    def __eq__(self, other):
        return self.point_id == other.point_id and self.longitude == other.longitude \
               and self.latitude == other.latitude and self.geohash == other.geohash

    def __repr__(self):
        return "Point({}, {}, {}, {})".format(self.point_id, self.latitude, self.longitude, self.geohash)


class PointWithDistance(Point):

    def __init__(self, point, distance):
        super().__init__(point.point_id, point.latitude, point.longitude)
        self.distance = distance

    def to_json(self):
        point_json = super().to_json()
        point_json["distance"] = self.distance
        return point_json

    def __eq__(self, other):
        return super().__eq__(other) and self.distance == other.distance

    def __repr__(self):
        return "PointWithDistance({}, {}, {}, {})".format(self.point_id, self.latitude, self.longitude, self.distance)
