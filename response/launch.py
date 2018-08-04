from .base_response import BaseResponse


class Launch(BaseResponse):
    def respond(self):
        speechlet_response = self.build_speechlet_response('football gossip',
                                                           "<speak>Hello and welcome to football gossip.</speak>",
                                                           True,
                                                           'Hello and welcome to football gossip',
                                                           'getGossip')

        return self.build_response({}, speechlet_response)


