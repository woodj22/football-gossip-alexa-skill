import unittest
from unittest import mock
from responses import RespondWithIntent


class TestIntentResponse(unittest.TestCase):

    @mock.patch('responses.gossip.get_gossip_as_ssml')
    def test_get_gossip_response_returns_correct_json(self, mock_get):
        mock_get.return_value = "<speak>test output</speak>"

        speechlet_response = {
            'outputSpeech': {
                'type': 'SSML',
                "ssml": "<speak>test output</speak>"
            },
            'card': {
                'type': 'Simple',
                'title': 'football gossip',
                'content': "Listen to the latest english football gossip."
            },
            'shouldEndSession': True,
        }

        expected_result = {
            'version': '1.0',
            'sessionAttributes': {},
            'response': speechlet_response
        }
        actual_result = RespondWithIntent().get_gossip_response()
        self.assertEqual(expected_result, actual_result)

    def test_get_help_response_returns_correct_json(self):
        speechlet_response = {
            'outputSpeech': {
                'type': 'SSML',
                "ssml": "<speak><s>You can say what's the gossip, or, you can say exit...</s> <s> What can I help you with?</s></speak>"
            },
            'card': {
                'type': 'Simple',
                'title': 'football gossip',
                'content': "Listen to the latest english football gossip."
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': "<speak><s>You can say what's the gossip, or, you can say exit...</s> <s> What can I help you with?</s></speak>"
                }
            },
            'shouldEndSession': False,
        }

        expected_result = {
            'version': '1.0',
            'sessionAttributes': {},
            'response': speechlet_response
        }

        actual_result = RespondWithIntent().get_help_response()
        self.assertEqual(expected_result, actual_result)

    def test_get_stop_response_returns_correct_json(self):
        speechlet_response = {
            'outputSpeech': {
                'type': 'SSML',
                "ssml": "<speak><s>Thank you for reading the gossip.</s><s> Have a pleasant day.</s></speak>"
            },
            'card': {
                'type': 'Simple',
                'title': 'Goodbye!',
                'content': "Listen to the latest english football gossip."
            },
            'shouldEndSession': True,
        }

        expected_result = {
            'version': '1.0',
            'sessionAttributes': {},
            'response': speechlet_response
        }

        actual_result = RespondWithIntent().get_stop_response()
        self.assertEqual(expected_result, actual_result)

    def test_get_fallback_response_response_returns_correct_json(self):
        speechlet_response = {
            'outputSpeech': {
                'type': 'SSML',
                "ssml": "<speak><s>The football gossip skill can't help you with that. </s><s> What can I help you with?</s></speak>"
            },
            'card': {
                'type': 'Simple',
                'title': 'What can I help you with?',
                'content': "Listen to the latest english football gossip."
            },
            'shouldEndSession': False,
        }

        expected_result = {
            'version': '1.0',
            'sessionAttributes': {},
            'response': speechlet_response
        }

        actual_result = RespondWithIntent().get_fallback_response()
        self.assertEqual(expected_result, actual_result)
