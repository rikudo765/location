from app.main.shared import logger
import time
import json
import werkzeug

from flask import Blueprint, jsonify, request, abort

from app.main.globals import storage, searcher, VERSION
from app.main.loc_types import Point

handler = Blueprint("location", __name__, url_prefix="/location/v1")


@handler.route('/healthcheck', methods=["GET"])
def health_check():
    return jsonify(status="green", version=VERSION), 200


@handler.route('/points', methods=['POST'])
def update():
    if not request.json:
        logger.error("invalid json")
        abort(400)

    point = Point.from_json(request.json)
    is_created = storage.set_point(point)
    logger.info("Point {0} was {1}".format(point.point_id, "created" if is_created else "updated"))

    return jsonify(point_id=point.point_id), 201 if is_created else 200


@handler.route('/points/<string:point_id>', methods=["GET"])
def get(point_id):
    point = storage.get_point(point_id)
    return point.to_json(), 200


@handler.route('/points/<string:point_id>', methods=["DELETE"])
def delete(point_id):
    storage.remove_point(point_id)
    logger.info("Point {0} has been removed".format(point_id))
    return jsonify(point_id=point_id), 200


@handler.route('/search', methods=["GET"])
def search():
    longitude = float(request.args["longitude"])
    latitude = float(request.args["latitude"])
    radius = int(request.args["radius"])

    start_time = time.time()

    prefix = searcher.general_prefix(Point("centre_point", latitude, longitude), radius)
    points = searcher.search_points(Point("centre_point", latitude, longitude), radius,
                                    storage.get_points_by_pref(prefix))
    total_time = time.time() - start_time
    logger.info("search with latitude {0} longitude {1} radius {2} found {3} points.Time: {4}".format(latitude,
                                                                                                      longitude,
                                                                                                      radius,
                                                                                                      len(points),
                                                                                                      total_time))
    result = {"request": {"longitude": longitude,
                          "latitude": latitude,
                          "radius": radius},
              "points": [p.to_json() for p in points]}

    return jsonify(result), 200


@handler.route('/search2', methods=["GET"])
def search_rectangle():
    rectangle = [Point("top_left_point", float(request.args["top_left_lat"]),
                       float(request.args["top_left_long"])),
                 Point("bottom_right_point", float(request.args["bottom_right_lat"]),
                       float(request.args["bottom_right_long"]))]
    current_point = Point("current_point", float(request.args["current_lat"]), float(request.args["current_long"]))

    start = time.time()
    prefix = searcher.general_prefix_rectangle(rectangle)
    points = searcher.search_points_rectangle(rectangle, current_point, storage.get_points_by_pref(prefix))
    total_time = time.time() - start

    logger.info("Search with top_left_long: [{0}];"
                " top_left_lat: [{1}];"
                " bottom_right_long: [{2}];"
                " bottom_right_lat: [{3}];"
                " current_long: [{4}];"
                " current_lat: [{5}] found {6} points. Time: {7}".format(rectangle[0].longitude,
                                                                         rectangle[0].latitude,
                                                                         rectangle[1].longitude,
                                                                         rectangle[1].latitude,
                                                                         current_point.longitude,
                                                                         current_point.latitude,
                                                                         len(points),
                                                                         total_time))
    result = {"points": [point.to_json() for point in points]}

    return jsonify(result), 200


@handler.app_errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"

    return response
