# -*- coding: utf-8 -*-
from requests_html import HTMLSession
import re

_speech_speed = '90%'
_gossip_url = "https://www.bbc.co.uk/sport/football/gossip"


def handler(event, context):
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.1001f962-280f-4cc9-a9f5-7888feba598c"):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    return


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getGossip":
        gossips = retrieve_gossip_strings(_gossip_url)
        return create_alexa_output(gossips, {'gossip_count': len(gossips)})
    else:
        raise ValueError("Invalid intent")


def retrieve_gossip_strings(url):
    session = HTMLSession()

    r = session.get(url)

    gossip_outer_class = r.html.find('#story-body', first=True)
    gossips = [re.sub("[\(\[].*?[\)\]]", "", p.text) for p in gossip_outer_class.find('p')]

    session.close()

    return gossips



def create_alexa_output(gossips, session_attributes):
    """Add SSML tags to gossips and remove all text in brackets"""

    ssml_gossip = ["<s><prosody rate=%s>" % _speech_speed + re.sub("[\(\[].*?[\)\]]", "", gossip) + "</prosody></s>" for
                   gossip in gossips]
    speech_output = "<speak>" + "".join(ssml_gossip) + "</speak>"

    return build_response(session_attributes, build_speechlet_response('getGossip', speech_output, True))


def build_speechlet_response(title, output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            "ssml": output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - The latest gossip"
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
