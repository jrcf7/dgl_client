import sys, os
from dgl_client.api_cli import APIClient

import unittest

# Set endpoint
DGL_API_ENDPOINT = "https://www.diglife.eu/"

class TestCollections(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        # Connect to the endpoint
        self.client = APIClient(DGL_API_ENDPOINT)    

        ACCESS_KEY=os.environ["DGL_TOK"]
        self.client.login(ACCESS_KEY)
        return 

    def test_list_collections(self):
        colls = self.client.collections.all()
        self.assertEqual(type(colls), list)

    def test_findcreate(self):
        COLL_TEST_NAME: str = "TEST1"
        coll = self.client.collections.find_or_create(COLL_TEST_NAME)
        self.assertEqual(coll.name, COLL_TEST_NAME)


if __name__ == '__main__':
    unittest.main()
