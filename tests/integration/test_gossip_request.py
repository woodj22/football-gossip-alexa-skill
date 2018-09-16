import unittest
from response.gossip_request import retrieve_gossip_strings


class TestGossipRequest(unittest.TestCase):

    def test_it_can_retrieve_an_array_of_gossip_strings(self):
        gossip_url = "https://www.bbc.co.uk/sport/football/gossip"

        response = retrieve_gossip_strings(gossip_url)
        print(response)
        self.assertIsInstance(response, list)
