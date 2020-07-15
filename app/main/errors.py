from werkzeug.exceptions import BadRequest, NotFound


class InvalidJson(BadRequest):
    def __init__(self, err):
        BadRequest.__init__(self, "Invalid json: {}".format(str(err)))


class InvalidType(BadRequest):
    def __init__(self, err):
        BadRequest.__init__(self, "Invalid type: {}".format(str(err)))


class PointNotFound(NotFound):
    def __init__(self, oid):
        NotFound.__init__(self, "Point {} not found".format(oid))


class EmptyStorage(NotFound):
    def __init__(self):
        NotFound.__init__(self, "Storage is empty")
