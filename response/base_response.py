_speech_speed = "'100%'"
from abc import ABC, abstractmethod


class BaseResponse(ABC):

    @abstractmethod
    def respond(self):
        speechlet_response = self.build_speechlet_response('football gossip',
                                      "<speak>Hello and welcome to football gossip.</speak>",
                                      True,
                                      'Hello and welcome to football gossip',
                                      'getGossip')

        return self.build_response({}, speechlet_response)

    @staticmethod
    def build_speechlet_response(title, ssml_output, should_end_session, card_speechlet_output, new_intent_name, directive_type="Dialog.ConfirmIntent", confirmation_status="NONE"):
        return {
            'outputSpeech': {
                'type': 'SSML',
                "ssml": ssml_output
            },
            'card': {
                'type': 'Simple',
                'title': title,
                'content': card_speechlet_output
            },
            'shouldEndSession': should_end_session,
            'directives': [{
                "type": directive_type,
                "updatedIntent": {
                    "name": new_intent_name,
                    "confirmationStatus": confirmation_status,
                }
            }]
        }

    @staticmethod
    def build_response(session_attributes, speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }
