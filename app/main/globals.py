import os

from app.main.storage import Storage
from app.main.searcher import Search


storage = Storage()
searcher = Search()

VERSION = "1.0"

if not os.getenv('TEST_MODE'):
    VERSION += ".{}".format(os.getenv("VERSION_TAG"))
