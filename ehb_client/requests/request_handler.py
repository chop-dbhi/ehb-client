from django.conf import settings

import httplib
import json
import datetime
import logging

log = logging.getLogger('ehb-client')


class RequestHandler(object):
    '''
    The Request Handler object is designed to allow making multiple requests from a fixed host
    '''

    def __init__(self, host, secure=False, api_key=None):
        self.host = host
        self.secure = secure
        self.lastrequestbody = ''
        self.api_key = api_key

    def append_key(self, headers):
        if headers:
            headers['Api-Token'] = self.api_key
        return headers

    def sendRequest(self, verb, path='', headers='', body=''):
        self.lastrequestbody = body
        if(self.secure):
            c = httplib.HTTPSConnection(self.host)
        else:
            c = httplib.HTTPConnection(self.host)
        headers = self.append_key(headers)
        if settings.DEBUG or settings.EHB_LOG:
            ts = datetime.datetime.now()
        c.request(verb, path, body, headers)
        if settings.DEBUG or settings.EHB_LOG:
            data = {
                'path': path,
                'response_time': (datetime.datetime.now() - ts).microseconds / 1000
            }
            log.debug("ehb request ({0}) {1}ms".format(
                data['path'],
                data['response_time']),
                extra=data)
        r = c.getresponse()
        return r

    def POST(self, path='', headers='', body=''):
        self.lastrequestbody = body
        return self.sendRequest('POST', path, headers, body)

    def GET(self, path='', headers=''):
        self.lastrequestbody = ''
        return self.sendRequest('GET', path, headers)

    def PUT(self, path='', headers='', body=''):
        self.lastrequestbody = body
        return self.sendRequest('PUT', path, headers, body)

    def DELETE(self, path='', headers=''):
        self.lastrequestbody = ''
        return self.sendRequest('DELETE', path, headers)

    def HEAD(self, path='', headers=''):
        self.lastrequestbody = ''
        return self.sendRequest('HEAD', path, headers)

    def OPTIONS(self, path='', headers='', body=''):
        self.lastrequestbody = ''
        return self.sendRequest('OPTIONS', path, headers, body)
