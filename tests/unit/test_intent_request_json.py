import unittest

from responses import RespondWithIntent


class TestIntentRequestJSON(unittest.TestCase):

    def test_it_can_create_response_with_correct_json(self):
        speechlet_response = {'test': 'resond with something'}
        session_attributes = {'test': 'session'}

        actual_json = RespondWithIntent._response(speechlet_response, session_attributes)

        self.assertEqual(actual_json['response'], speechlet_response)
        self.assertEqual(actual_json['sessionAttributes'], session_attributes)
        self.assertIn('version', actual_json)

    def test_it_can_build_speechlet_response_with_correct_keys_in_json(self):
        title = 'hello test title'
        output = "<speak>exmaple ssml output</speak>"
        end_session = True
        actual_json = RespondWithIntent._build_speechlet_response(title, output, end_session)

        self.assertEqual(actual_json['outputSpeech']['ssml'], output)
        self.assertEqual(actual_json['outputSpeech']['type'], 'SSML')
        self.assertEqual(actual_json['card']['type'], 'Simple')
        self.assertEqual(actual_json['card']['title'], title)
        self.assertEqual(actual_json['card']['content'], "Listen to the latest english football gossip.")
        self.assertEqual(actual_json['shouldEndSession'], end_session)

    def test_it_can_build_speechlet_with_reprompt_response_with_correct_keys_in_json(self):
        title = 'hello test title'
        output = "<speak>exmaple ssml output</speak>"
        reprompt_text = 'This is reprompt text'
        end_session = True
        actual_json = RespondWithIntent. \
            _build_speechlet_with_reprompt_response(
            title,
            output,
            reprompt_text,
            end_session
        )

        self.assertEqual(actual_json['outputSpeech']['ssml'], output)
        self.assertEqual(actual_json['outputSpeech']['type'], 'SSML')
        self.assertEqual(actual_json['card']['type'], 'Simple')
        self.assertEqual(actual_json['card']['title'], title)
        self.assertEqual(actual_json['card']['content'], "Listen to the latest english football gossip.")
        self.assertEqual(actual_json['reprompt']['outputSpeech']['type'], 'SSML')
        self.assertEqual(actual_json['reprompt']['outputSpeech']['ssml'], reprompt_text)
        self.assertEqual(actual_json['shouldEndSession'], end_session)


