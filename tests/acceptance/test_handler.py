import os
import json
import unittest
from handler import handler


class TestHandler(unittest.TestCase):

    def _get_json_file(self, file_name):
        relative_path = '../mock_requests/' + file_name

        script_dir = os.path.dirname(__file__)

        file_path = os.path.join(script_dir, relative_path)

        with open(file_path, 'r') as f:
            return json.load(f)

    def test_it_can_send_a_get_gossip_intent_json_and_respond_with_correct_json(self):
        file = self._get_json_file('get_gossip_intent_request.json')

        actual_response = handler(file, {})

        self.assertIn('version', actual_response)
        self.assertIn('sessionAttributes', actual_response)
        self.assertIn('response', actual_response)

    def test_it_can_send_launch_request_json_and_respond_with_correct_json(self):
        file = self._get_json_file('launch_request.json');

        actual_response = handler(file, {})

        self.assertIn('version', actual_response)
        self.assertIn('sessionAttributes', actual_response)
        self.assertIn('response', actual_response)

    def test_it_can_throw_a_value_error_when_request_type_is_not_recognised(self):
        file = {
            'session': {
                'application': {
                    'applicationId': "amzn1.ask.skill.1001f962-280f-4cc9-a9f5-7888feba598c"
                }
            },
            'request': {
                'type': 'AnotherRequestTypeThat is invalid'
            }
        }
        with self.assertRaises(ValueError):
            handler(file, {})


