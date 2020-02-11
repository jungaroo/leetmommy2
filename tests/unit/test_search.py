import unittest
from lib.search import IndexController
from lib.config import CONFIG

# Mock elastic search api
class IndexControllerTest(unittest.TestCase):
    """Tests search methods of IndexController class of search"""
    # Probably test things like, checking it's a singleton