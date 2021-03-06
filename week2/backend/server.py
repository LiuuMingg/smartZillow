import json
import os
import pyjsonrpc
import re
import sys

from bson.json_util import dumps

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

PROPERTY_TABLE_NAME = 'property'

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test method"""
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add gets called with %d and %d" % (a, b)
        return a + b

    """Search properties in an area by zipcode or city/state"""
    @pyjsonrpc.rpcmethod
    def searchArea(self, query):
        res = []
        if query.isdigit():
            db = mongodb_client.getDB()
            res = db[PROPERTY_TABLE_NAME].find({'zipcode': query})
            res = json.loads(dumps(res))
        else:
            city = query.split(',')[0].strip()
            state = query.split(',')[1].strip()
            db = mongodb_client.getDB()
            # Use regular expression to do case-insensitive search.
            res = db[PROPERTY_TABLE_NAME].find({'city': re.compile(city, re.IGNORECASE),
                                                'state': re.compile(state, re.IGNORECASE)})
            res = json.loads(dumps(res))
        return res

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server..."
print "Listening on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
