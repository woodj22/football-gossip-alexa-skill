# -*- coding: utf-8 -*-
from requests_html import HTMLSession
import re

SPEECH_SPEED = "'100%'"
GOSSIP_URL = "https://www.bbc.co.uk/sport/football/gossip"


def handler(event, context):
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.1001f962-280f-4cc9-a9f5-7888feba598c"):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    return


def on_launch(launch_request, session):
    return get_gossip_response("ACCEPT", session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent_name = intent_request['intent']['name']

    if intent_name == "getGossip":
        return get_gossip_response()
    if intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    if intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    if intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    if intent_name == "AMAZON.YesIntent":
        return get_gossip_response()
    if intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else:
        raise ValueError("Invalid intent")

def get_gossip_response():
    gossips = retrieve_gossip_strings(GOSSIP_URL)

    return create_alexa_gossip_output(gossips)


def get_help_response():
    """ Help response must end in a question. Amazon rules."""
    output = "<speak><s>You can say get me the gossip, or, you can say exit... What can I help you with?</s></speak>"

    return response(build_speechlet_with_prompt_response(output, output, False))


def get_stop_response():
    """ end the session."""
    speech_output = "<speak><s>Thank you for reading the gossip.</s><s> Have a pleasant day.</s></speak>"

    return response(build_speechlet_response('Goodbye!', speech_output, True))


def get_fallback_response():
    output = "The football gossip skill can't help you with that. . What can I help you with?"

    return response(build_speechlet_response("What can I help you with?", output, False))


def retrieve_gossip_strings(url):
    session = HTMLSession()

    r = session.get(url)

    gossip_outer_class = r.html.find('#story-body', first=True)
    gossips = [re.sub("[\(\[].*?[\)\]]", "", p.text) for p in gossip_outer_class.find('p')]

    session.close()

    return gossips


def create_alexa_gossip_output(gossips, session):
    """Add SSML tags to gossips and remove all text in brackets"""

    speech_output = build_gossip_ssml_string(gossips)

    return response(build_speechlet_response('football gossip', speech_output, True))


def build_gossip_ssml_string(gossips):
    ssml_gossip = ["<p><prosody rate=%s>" % SPEECH_SPEED + re.sub("[\(\[].*?[\)\]]", "", gossip) + "</prosody></p>" for
                   gossip in gossips]

    return "<speak>" + "".join(ssml_gossip) + "</speak>"


def build_speechlet_response(title, output, end_session):
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


def build_speechlet_with_prompt_response(output, reprompt_text, end_session):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'text': reprompt_text
            }
        },
        'shouldEndSession': end_session
    }


def response(speechlet_response, session_attributes={}):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
