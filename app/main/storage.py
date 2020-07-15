from app.main import errors
from app.main.shared import logger
from google.cloud import firestore
from app.main.loc_types import Point


class Storage:

    def __init__(self):
        self.collection = None

    def init_app(self, test_mode):
        client = firestore.Client()
        if test_mode:
            self.collection = client.collection('TestLocation')
        else:
            self.collection = client.collection('Location')

        logger.info("started firestore: project={}, collection={}".format(client.project, self.collection.id))

    def set_point(self, point):
        ref = self.collection.document(point.point_id)
        exists = ref.get().exists
        ref.set(point.to_json(), merge=True)

        return not exists

    def get_point(self, point_id):
        doc = self.collection.document(point_id).get()
        if not doc.exists:
            raise errors.PointNotFound(point_id)

        point = Point.from_json(doc.to_dict())
        return point

    def remove_point(self, point_id):
        ref = self.collection.document(point_id)
        if not ref.get().exists:
            raise errors.PointNotFound(point_id)

        ref.delete()

    # return: list of dicts. dict : information about point
    def get_points_by_pref(self, prefix):
        docs = self.collection.where('geohash', '>=', prefix).where('geohash', '<=', prefix + 'zzzz').stream()
        all_points = []
        for doc in docs:
            point = doc.to_dict()
            try:
                all_points.append(Point.from_json(point))
            except errors.InvalidJson:
                logger.error("found invalid point: {}".format(point))

        return all_points
