# -*- coding: utf-8 -*-

from response import RespondWithIntent

def handler(event, context):
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.1001f962-280f-4cc9-a9f5-7888feba598c"):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    return


def on_launch(request, session):
    """ called on Launch."""
    return RespondWithIntent().get_gossip_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent_name = intent_request['intent']['name']
    responder = RespondWithIntent()
    if intent_name == "GetGossipIntent":
        return responder.get_gossip_response()
    if intent_name == "AMAZON.HelpIntent":
        return responder.get_help_response()
    if intent_name == "AMAZON.StopIntent":
        return responder.get_stop_response()
    if intent_name == "AMAZON.CancelIntent":
        return responder.get_stop_response()
    if intent_name == "AMAZON.FallbackIntent":
        return responder.get_fallback_response()
    else:
        raise ValueError("Invalid intent")

