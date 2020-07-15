import unittest
from app.main.searcher import Search
from app.main.loc_types import Point, PointWithDistance


class TestSearcher(unittest.TestCase):

    def test_on_empty_list_circle(self):
        self.assertEqual(Search.search_points(Point("", 46.483264729155586, 30.731506347656254), 3, []), [])

    def test_with_radius_increase_circle(self):
        points = [Point("1.00", 49.86875093132386, -126.63013458251955),
                  Point("1.04", 49.86460165007597, -126.61710977554323),
                  Point("2.04", 49.86512724541457, -126.61693811416627),
                  Point("3.26", 49.86431118704076, -126.61401987075807),
                  Point("4.22", 49.8661784189361, -126.61363363265993),
                  Point("5.45", 49.86283118159863, -126.6121530532837),
                  Point("6.37", 49.86399305885544, -126.61258220672609),
                  Point("7.205", 49.857823724196905, -126.60713195800783)]

        self.assertEqual(len(Search.search_points(Point("", 49.86875093132386, -126.63013458251955), 0, points)), 1)

        self.assertEqual(len(Search.search_points(Point("", 49.86875093132386, -126.63013458251955), 1100, points)), 3)

        self.assertEqual(len(Search.search_points(Point("", 49.86875093132386, -126.63013458251955), 1300, points)), 5)

        self.assertEqual(len(Search.search_points(Point("", 49.86875093132386, -126.63013458251955), 1400, points)), 6)

        self.assertEqual(len(Search.search_points(Point("", 49.86875093132386, -126.63013458251955), 1500, points)), 7)

        self.assertEqual(len(Search.search_points(Point("", 49.86875093132386, -126.63013458251955), 2100, points)), 8)

    def test_in_or_not_in_circle(self):
        res = Search.search_points(Point("", 17.43215425542, 63.3124235462342), 1000,
                                   [Point("1", 17.42565123123, 63.325814352343),
                                    Point("2", 17.42565123123, 63.325814352343)])
        self.assertEqual(res, [])

    def test_with_distance_circle(self):
        points_list = [Point("1.04", 49.98460165007597, -126.61710977554323),
                       Point("2.04", 49.97512724541457, -126.61693811416627),
                       Point("3.26", 49.96431118704076, -126.61401987075807),
                       Point("4.22", 49.9061784189361, -126.61363363265993),
                       Point("5.45", 49.86383118159863, -126.6121530532837),
                       Point("6.37", 49.86499305885544, -126.61258220672609),
                       Point("7.205", 49.857823724196905, -126.60713195800783)]

        res = Search.search_points(Point("", 49.86431118704076, -126.6171530532837), 5000, points_list)

        expected_list = [PointWithDistance(points_list[5], 336),
                         PointWithDistance(points_list[4], 362),
                         PointWithDistance(points_list[6], 1018),
                         PointWithDistance(points_list[3], 4662)]

        self.assertEqual(res, expected_list)

    def test_general_prefix_circle(self):
        point = Point("test_id", 19.97512724541457, 24.61693811416627)
        self.assertTrue(Search.general_prefix(Point("", 19.97512724541457, 24.61693811416627), 800) in point.geohash)

        self.assertEqual(Search.general_prefix(Point("", 49.98460165007597, -126.61710977554323), 500), "c0vuq")
        self.assertEqual(Search.general_prefix(Point("", 49.97512724541457, -126.61693811416627), 800), "c0vu")
        self.assertEqual(Search.general_prefix(Point("", 49.97512724541457, -126.61693811416627), 4000), "c0")
        self.assertEqual(Search.general_prefix(Point("", 49.97512724541457, -126.61693811416627), 90000), "c")

        self.assertEqual(Search.general_prefix(Point("", 32.97512724541457, -57.61693811416627), 1000), "dtz5")
        self.assertEqual(Search.general_prefix(Point("", 46.97512724541457, 47.61693811416627), 5000), "v03")
        self.assertEqual(Search.general_prefix(Point("", 46.97512724541457, 63.61693811416627), 3000), "v2m")

    def test_general_prefix_rectangle(self):
        actual = Search.general_prefix_rectangle([Point("top_left", 59.72386952131737, -113.01773071289062),
                                                  Point("bot_right", 59.68386129364914, -112.92572021484375)])
        self.assertEqual("c6xe", actual)

        actual = Search.general_prefix_rectangle([Point("top_left", 59.839295488500326, -112.89825439453125),
                                                  Point("bot_right", 59.78577919120723, -112.79525756835938)])
        self.assertEqual("c6x", actual)

        actual = Search.general_prefix_rectangle([Point("top_left", 60.2035192283986, -112.91772723197937),
                                                  Point("bot_right", 60.20343925759669, -112.91756093502045)])
        self.assertEqual("c6xwqrxy", actual)

        actual = Search.general_prefix_rectangle([Point("top_left", 60.13586367528046, -112.8738784790039),
                                                  Point("bot_right", 60.13458148138504, -112.87078857421875)])
        self.assertEqual("c6xwp", actual)

    def test_search_in_rectangle(self):
        points = [Point("in_rect1", 59.708114412194135, -112.99713134765625),
                  Point("in_rect2", 59.692871645401674, -112.99198150634766),
                  Point("in_rect3", 59.697029451864545, -112.9669189453125),
                  Point("in_rect4", 59.71313607653958, -112.97309875488281),
                  Point("in_rect5", 59.72213855345352, -113.00537109375),
                  Point("not_in_rect1", 59.7363298459524, -112.95249938964844),
                  Point("not_in_rect2", 59.6673938144924, -112.97138214111328),
                  Point("not_in_rect3", 59.70361158972945, -112.88108825683594),
                  Point("not_in_rect4", 59.7037847864095, -113.05103302001953),
                  Point("not_in_rect5", 59.72767733532802, -113.01155090332031)]
        actual = len(Search.search_points_rectangle([Point("top_left", 59.72386952131737, -113.01773071289062),
                                                     Point("bot_right", 59.68386129364914, -112.92572021484375)],
                                                    Point("cur_p", 59.70222598402985, -112.9562759399414), points))
        self.assertEqual(5, actual)

    def test_with_distance_rectangle(self):
        points = [Point("in_rect1", 59.708114412194135, -112.99713134765625),
                  Point("in_rect2", 59.692871645401674, -112.99198150634766),
                  Point("in_rect3", 59.697029451864545, -112.9669189453125),
                  Point("in_rect4", 59.71313607653958, -112.97309875488281),
                  Point("in_rect5", 59.72213855345352, -113.00537109375),
                  Point("not_in_rect1", 59.7363298459524, -112.95249938964844),
                  Point("not_in_rect2", 59.6673938144924, -112.97138214111328),
                  Point("not_in_rect3", 59.70361158972945, -112.88108825683594),
                  Point("not_in_rect4", 59.7037847864095, -113.05103302001953),
                  Point("not_in_rect5", 59.72767733532802, -113.01155090332031)]

        actual = Search.search_points_rectangle([Point("top_left", 59.72386952131737, -113.01773071289062),
                                                 Point("bot_right", 59.68386129364914, -112.92572021484375)],
                                                Point("cur_p", 59.70222598402985, -112.9562759399414), points)

        expected_list = [PointWithDistance(points[2], 830),
                         PointWithDistance(points[3], 1536),
                         PointWithDistance(points[1], 2257),
                         PointWithDistance(points[0], 2383),
                         PointWithDistance(points[4], 3533)]

        self.assertEqual(expected_list, actual)


if __name__ == '__main__':
    unittest.main()
