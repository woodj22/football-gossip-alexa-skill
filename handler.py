
# -*- coding: utf-8 -*-
from requests_html import HTMLSession

def build_speechlet_response(title, output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            "ssml": output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def retrieve_gossip_strings(url):
    session = HTMLSession()
    r = session.get(url)

    gossips = r.html.find('#story-body', first=True)
    gossip = [p.text for p in gossips.find('p')]

    session.close()

    return gossip


def output_alexa_audio(gossips, session_attributes):
        speech_output = "<speak>" + "<s>".join(gossips) + "</speak>"

        return build_response(session_attributes,  build_speechlet_response('getGossip', speech_output, True))


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getGossip":
         gossips = retrieve_gossip_strings("https://www.bbc.co.uk/sport/football/gossip")
         return output_alexa_audio(gossips, {'gossip_count': len(gossips)})
    else:
        raise ValueError("Invalid intent")



def handler(event, context):
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.1001f962-280f-4cc9-a9f5-7888feba598c"):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    return

if __name__ == "__main__":
    handler('', '')


