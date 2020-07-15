from app.main.geohash import encode
from math import cos, asin, sin, pi, sqrt
from app.main.loc_types import PointWithDistance


def in_circle_check(point_to_check, centre_point, radius):

    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((centre_point.latitude - point_to_check.latitude) * p) / 2 + cos(point_to_check.latitude * p) * \
        cos(centre_point.latitude * p) * \
        (1 - cos((centre_point.longitude - point_to_check.longitude) * p)) / 2
    distance = int(12742 * asin(sqrt(a)) * 1000)  # 2*R*asin...#*1000- meters

    if distance <= radius:
        return distance, True

    return 0, False


def in_rectangle_check(rectangle, current_point, point_for_check):

    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((current_point.latitude - point_for_check.latitude) * p) / 2 + cos(point_for_check.latitude * p) * \
        cos(current_point.latitude * p) * (1 - cos((current_point.longitude - point_for_check.longitude) * p)) / 2
    distance = int(12742 * asin(sqrt(a)) * 1000)

    if (rectangle[0].longitude <= point_for_check.longitude <= rectangle[1].longitude) and \
            (rectangle[1].latitude <= point_for_check.latitude <= rectangle[0].latitude):
        return distance, True

    return 0, False


class Search:

    # return: common prefix
    @staticmethod
    def str_first_intersection(raw1, raw2, raw3, raw4):
        new_raw = ""
        for i in range(len(raw1)):
            if raw1[i] == raw2[i] and raw1[i] == raw3[i] and raw1[i] == raw4[i]:
                new_raw += raw1[i]
            else:
                break
        return new_raw

    @staticmethod
    def general_prefix_rectangle(rectangle):

        left_top = encode(rectangle[0].latitude, rectangle[0].longitude)
        left_bottom = encode(rectangle[1].latitude, rectangle[0].longitude)
        right_top = encode(rectangle[0].latitude, rectangle[1].longitude)
        right_bottom = encode(rectangle[1].latitude, rectangle[1].longitude)

        return Search.str_first_intersection(left_top, left_bottom, right_top, right_bottom)

    @staticmethod
    def search_points_rectangle(rectangle, current_point, points):
        res = []
        for point_for_check in points:
            distance, ok = in_rectangle_check(rectangle, current_point, point_for_check)
            if ok:
                res.append(PointWithDistance(point_for_check, distance))

        return sorted(res, key=lambda pt: pt.distance)

    # QUERY CIRCLE (latitude, longitude, distance)
    # minimum bounding rectangle contains QUERY CIRCLE
    # return : common prefix of all points from minimum bounding rectangle
    @staticmethod
    def general_prefix(centre_point, distance):
        # d - angular radius
        d = distance / 6371000.0

        # latitude and longitude in radians
        lat_rad = centre_point.latitude * pi / 180
        long_rad = centre_point.longitude * pi / 180

        delta_long = asin(sin(d) / cos(lat_rad))

        # max/min latitude and longitude (degrees)
        long_min = (long_rad - delta_long) * 180 / pi
        long_max = (long_rad + delta_long) * 180 / pi
        lat_min = (lat_rad - d) * 180 / pi
        lat_max = (lat_rad + d) * 180 / pi

        # Four vertices of the minimum bounding rectangle that fully contains QUERY CIRCLE
        north_west = encode(lat_max, long_min)
        south_west = encode(lat_min, long_min)
        south_east = encode(lat_min, long_max)
        north_east = encode(lat_max, long_max)

        return Search.str_first_intersection(north_east, south_east, north_west, south_west)

    @staticmethod
    def search_points(centre_point, radius, points):
        res = []
        for point_for_check in points:
            distance, ok = in_circle_check(point_for_check, centre_point, radius)
            if ok:
                res.append(PointWithDistance(point_for_check, distance))

        return sorted(res, key=lambda pt: pt.distance)
