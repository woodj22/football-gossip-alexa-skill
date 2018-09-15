from requests_html import HTMLSession
import re

SPEECH_SPEED = "'100%'"
GOSSIP_URL = "https://www.bbc.co.uk/sport/football/gossip"


def get_gossip_as_ssml():
    gossips = retrieve_gossip_strings(GOSSIP_URL)

    return build_ssml_string(gossips)


def retrieve_gossip_strings(url):
    session = HTMLSession()

    r = session.get(url)

    gossip_outer_class = r.html.find('#story-body', first=True)
    gossips = [re.sub("[\(\[].*?[\)\]]", "", p.text) for p in gossip_outer_class.find('p')]

    session.close()

    return gossips


def build_ssml_string(gossips):
    ssml_gossip = ["<p><prosody rate=%s>" % SPEECH_SPEED + re.sub("[\(\[].*?[\)\]]", "", gossip) + "</prosody></p>"
                   for
                   gossip in gossips]

    return "<speak>" + "".join(ssml_gossip) + "</speak>"
