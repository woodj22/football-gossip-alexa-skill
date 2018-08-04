# -*- coding: utf-8 -*-
from requests_html import HTMLSession
import re

_speech_speed = "'100%'"
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
    confirmation = intent_request['intent']['confirmationStatus']
    if intent_name == "getGossip":
        if confirmation == 'DENIED':
            return create_goodbye_output()
        gossips = retrieve_gossip_strings(_gossip_url)
        return create_alexa_gossip_output(gossips, session)
    else:
        raise ValueError("Invalid intent")


def create_goodbye_output():
    speech_output = "<speak><s>Thank you for reading the gossip.</s><s>Have a pleasant day.</s></speak>"

    return build_response({}, build_speechlet_response('goodbye!', speech_output, True))


def retrieve_gossip_strings(url):
    session = HTMLSession()

    r = session.get(url)

    gossip_outer_class = r.html.find('#story-body', first=True)
    gossips = [re.sub("[\(\[].*?[\)\]]", "", p.text) for p in gossip_outer_class.find('p')]

    session.close()

    return gossips


def create_alexa_gossip_output(gossips, session):
    """Add SSML tags to gossips and remove all text in brackets"""
    try:
        session_start = session['attributes']['currentGossipIndex']
    except KeyError:
        session_start = 0

    session_end = session_start + 5

    if session_end > len(gossips):
        session_end = len(gossips)

        should_end_session = True
        suffix_sentence = 'That is all the gossip for today. Goodbye!'
    else:
        should_end_session = False
        suffix_sentence = 'Would you like me to continue?'

    sliced_gossips = gossips[session_start:session_end]

    speech_output = build_gossip_ssml_string(sliced_gossips, suffix_sentence)
    session_attributes = {'currentGossipIndex': session_end}

    return build_response(session_attributes, build_speechlet_response('football gossip', speech_output, should_end_session))


def build_gossip_ssml_string(gossips, suffix_sentence):
    ssml_gossip = ["<p><prosody rate=%s>" % _speech_speed + re.sub("[\(\[].*?[\)\]]", "", gossip) + "</prosody></p>" for
                   gossip in gossips]

    return "<speak>" + "".join(ssml_gossip) + suffix_sentence + "</speak>"


def build_speechlet_response(title, output, should_end_session):
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
        'shouldEndSession': should_end_session,
        'directives': [{
            "type": "Dialog.ConfirmIntent",
            "updatedIntent": {
                "name": "getGossip",
                "confirmationStatus": "NONE",
            }
        }]
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
