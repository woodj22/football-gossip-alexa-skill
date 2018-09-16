from response import gossip_request


class RespondWithIntent:

    def get_gossip_response(self):
        speech_output = gossip_request.get_gossip_as_ssml()

        return self._response(self._build_speechlet_response('football gossip', speech_output, True))

    def get_help_response(self):
        """ Help response must end in a question. Amazon rules."""
        output = "<speak><s>You can say what's the gossip, or, you can say exit...</s> <s> What can I help you with?</s></speak>"

        return self._response(self._build_speechlet_with_reprompt_response('football gossip', output, output, False))

    def get_stop_response(self):
        """ end the session."""
        speech_output = "<speak><s>Thank you for reading the gossip.</s><s> Have a pleasant day.</s></speak>"

        return self._response(self._build_speechlet_response('Goodbye!', speech_output, True))

    def get_fallback_response(self):
        output = "<speak><s>The football gossip skill can't help you with that. </s><s> What can I help you with?</s></speak>"

        return self._response(self._build_speechlet_response("What can I help you with?", output, False))

    @staticmethod
    def _build_speechlet_response(title, output, end_session):
        return {
            'outputSpeech': {
                'type': 'SSML',
                "ssml": output
            },
            'card': {
                'type': 'Simple',
                'title': title,
                'content': "Listen to the latest english football gossip."
            },
            'shouldEndSession': end_session,
        }

    @staticmethod
    def _build_speechlet_with_reprompt_response(title, output, reprompt_text, end_session):
        """ create a simple json response with a prompt """

        return {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': output
            },
            'card': {
                'type': 'Simple',
                'title': title,
                'content': "Listen to the latest english football gossip."
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': reprompt_text
                }
            },
            'shouldEndSession': end_session
        }

    @staticmethod
    def _response(speechlet_response, session_attributes={}):
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }
