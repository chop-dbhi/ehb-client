from http import client
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
            c = client.HTTPSConnection(self.host)
        else:
            c = client.HTTPConnection(self.host)
        headers = self.append_key(headers)
        c.request(verb, path, body, headers)
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
