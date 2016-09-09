from ehb_client.requests.request_handler import RequestHandler
from ehb_client.requests.exceptions import PageNotFound, ServerError, \
    MalformedRequestBody, RequestedRangeNotSatisfiable, NotAuthorized
import datetime
from abc import ABCMeta, abstractmethod
import json
import re


class abstractstatic(staticmethod):

    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


class IdentityBase(object, metaclass=ABCMeta):

    @abstractstatic
    def findIdentity(searchTermsDict, *identities):
        pass

    @abstractstatic
    def identityLabel():
        # When implemented this must be the label used by the ehb-service in it's response
        pass

    @abstractstatic
    def identity_from_json(identityJsonString):
        pass

    @abstractstatic
    def json_from_identity(identity):
        pass

    # Concrete Methods
    def __eq__(self, other):
        if type(self).__name__ == 'NoneType':
            return type(other).__name__ == 'NoneType'
        elif type(other).__name__ == 'NoneType':
            return False
        b = True
        for k in list(self.__dict__.keys()):
            if k != 'modified' and k != 'created':
                b = b and self.__dict__.get(k) == other.__dict__.get(k)
        return b

    def __ne__(self, other):
        return not self.__eq__(other)


class RequestBase(object, metaclass=ABCMeta):
    def __init__(self, host, root_path='', secure=False, api_key=None):
        self.host = host
        self.secure = secure
        self.request_handler = RequestHandler(host, secure, api_key)
        self.root_path = root_path

    # Abstract
    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass

    @abstractmethod
    def create(self, *objects):
        pass

    @abstractmethod
    def update(self, *objects):
        pass

    # Concrete
    def processResponse(self, response, path=''):
        status = response.status
        if status == 200:
            return response.read().decode('utf-8')
        elif status == 204:
            return response.read().decode('utf-8')
        elif status == 403:
            raise NotAuthorized
        elif status == 404:
            raise PageNotFound(path=path)
        elif status == 500:
            raise ServerError
        elif status == 422:
            raise MalformedRequestBody(self.request_handler.lastrequestbody)
        elif status == 416:
            split = path.split('?')
            gr = None
            if len(split) == 2:
                gr = split[1]
            raise RequestedRangeNotSatisfiable(gr)
        else:
            msg = "Unknown Response Code From Server: {0}".format(status)
            raise Exception(msg)

    @staticmethod
    def dateFromString(yyyymmdd, delim='-'):
        v = yyyymmdd.split(delim)
        year = int(v[0])
        month = int(v[1])
        day = int(v[2])
        return datetime.date(year, month, day)

    @staticmethod
    def timeFromString(hhmmss, delim=':'):
        v = hhmmss.split(delim)
        hour = int(v[0])
        minute = int(v[1])
        sec = int(v[2])
        return datetime.time(hour, minute, sec)

    @staticmethod
    def dateTimeFromJsonString(jsonString):
        if re.search(r'(\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d+)', jsonString):
            return datetime.datetime.strptime(jsonString, '%Y-%m-%d %H:%M:%S.%f')
        elif re.search(r'(\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', jsonString):
            return datetime.datetime.strptime(jsonString, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def stringFromDate(date, delim='-'):
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        return year + delim + month + delim + day

    @staticmethod
    def stringFromTime(time, delim=':'):
        hh = str(time.hour)
        mm = str(time.minute)
        ss = str(time.second)
        return hh + delim + mm + delim + ss


class JsonRequestBase(RequestBase, metaclass=ABCMeta):

    accept_json = {'Accept': 'application/json'}
    content_type_json = {'Content-Type': 'application/json'}

    def standardCreate(self, identityBase, successFunc, *identities):
        '''
        Given an arbitrary number of Identity objects of type X(IdentityBase),
        this method attempts to create the identity objects in the server database.
        Inputs:
          * identityBase: The Class object that extends IdentityBase
          * successFunc: a function that accepts an object, i, of type
                      identityBase and a dictionary of values that can be used
                      to populate i. Typically these will be values provided by
                      the server after creation, e.g. created date. The return
                      value of this function is not used
          * identities: the identity objects to be loaded from to the server
        Output:
          * List of dictionaries :
                                  {
                                    identityBase.identityLabel:identity object,
                                    "success":boolean,
                                    "errors":errors
                                   }
                                  where errors is None if there were no errors
                                  in creating the object in the server db
         '''

        path = self.root_path

        body = '['

        for i in identities:
            body += identityBase.json_from_identity(i) + ','

        body = body[0:body.__len__() - 1] + ']'
        response = self.processPost(path, body)
        status = []

        for o in json.loads(response):

            success = o.get('success')
            i = identityBase.findIdentity(o, *identities)

            if(success):
                successFunc(i, o)
                status.append({
                    identityBase.identityLabel: i,
                    "success": True,
                    "errors": None})
            else:

                errs = o.get('errors')
                errors = []

                for e in errs:
                    for k in list(e.keys()):
                        errors.append(e.get(k))

                status.append({
                    identityBase.identityLabel: i,
                    "success": False,
                    "errors": errors})
        return status

    def standardUpdate(self, identityBase, successFunc, *identities):
        '''
        Given an arbitrary number of Identity objects of type X(IdentityBase),
        this method attempts to updated the identity objects in the server database.
        Inputs:
          * identityBase: The Class object that extends IdentityBase
          * successFunc: a function that accepts an object, i, of type identityBase
                         and a dictionary of values that can be used to populate
                         i. Typically these will be values provided by the server
                         after creation, e.g. created date. The return value of
                         this function is not used.
          * identities: the identity objects to be loaded from to the server
        Output:
          * List of dictionaries :
                                  {
                                    identityBase.identityLabel:identity object,
                                    "success":boolean,
                                    "errors":errors
                                   }
                                  where errors is None if there were no errors
                                  in creating the object in the server db
        '''

        path = self.root_path
        body = '['

        for i in identities:
            id = i.id
            body += '{"id":"' + str(id) + '","' + identityBase.identityLabel + '":' + identityBase.json_from_identity(i) + '},'

        body = body[0:body.__len__() - 1] + ']'
        response = self.processPut(path, body)
        status = []
        for o in json.loads(response):

            success = o.get('success')
            i = identityBase.findIdentity(o, *identities)

            if(success):
                successFunc(i, o)
                status.append({identityBase.identityLabel: i, "success": True, "errors": None})
            else:
                errs = o.get('errors')
                errors = []
                for e in errs:
                    for k in list(e.keys()):
                        errors.append(e.get(k))
                status.append({identityBase.identityLabel: i, "success": False, "errors": errors})
        return status

    def processPost(self, path, body, headers={'Content-Type': 'application/json'}):
        upr = self.request_handler.POST(path=path, body=body, headers=headers)
        return self.processResponse(upr, path)

    def processGet(self, path, headers={'Accept': 'application/json'}):
        upr = self.request_handler.GET(path=path, headers=headers)
        return self.processResponse(upr, path)

    def processPut(self, path, body, headers={'Content-Type': 'application/json'}):
        upr = self.request_handler.PUT(path=path, headers=headers, body=body)
        return self.processResponse(upr, path)

    def processDelete(self, path, headers={'Accept': 'application/json'}):
        upr = self.request_handler.DELETE(path=path, headers=headers)
        return self.processResponse(upr, path)
