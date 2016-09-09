from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
import json
from ehb_client.requests.exceptions import PageNotFound, InvalidArguments
from ehb_client.requests.subject_request_handler import Subject
from ehb_client.requests.external_record_request_handler import ExternalRecord


class ExternalSystem(IdentityBase):

    def __init__(self, name, description, url, modified=None, created=None, id=-1):
        self.name = name
        self.description = description
        # Django always ensures that the ExternalSystem model url field ends in a '/'
        # so to prevent endless hours of wasted time debugging it is useful to ensure
        # the same here
        self.url = ExternalSystem.correctUrl(url)
        self.modified = modified
        self.created = created
        self.id = id

    @staticmethod
    def correctUrl(url):
        if not url.endswith('/'):
            url += '/'
        return url

    @staticmethod
    def findIdentity(searchTermsDict, *identities):
        id = searchTermsDict.get("id", None)
        if id:
            for s in identities:
                if s.id == int(id):
                    return s
        n = searchTermsDict.get("name", None)
        if n:
            for s in identities:
                if s.name == n:
                    return s
        u = searchTermsDict.get('url', None)
        if u:
            for s in identities:
                if s.url == u:
                    return s
        return None

    @staticmethod
    def identity_from_json(esJsonString):
        jsonObj = json.loads(esJsonString)
        return ExternalSystem.identity_from_jsonObject(jsonObj)

    @staticmethod
    def identity_from_jsonObject(jsonObj):
        n = jsonObj.get('name')
        des = jsonObj.get('description')
        u = jsonObj.get('url')
        lm = RequestBase.dateTimeFromJsonString(jsonObj.get('modified'))
        c = RequestBase.dateTimeFromJsonString(jsonObj.get('created'))
        id = int(jsonObj.get('id'))
        return ExternalSystem(name=n, description=des, url=u, modified=lm, created=c, id=id)

    @staticmethod
    def json_from_identity(es):
        q = '"'
        n = '"name":"' + es.name + q
        des = '"description":"' + es.description + q
        u = '"url":"' + es.url + q
        return '{' + n + ',' + des + ',' + u + '}'

    identityLabel = "external_system"


class ExternalSystemRequestHandler(JsonRequestBase):

    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, root_path+'/api/externalsystem/', secure, api_key)

    def query(self, *params):
        '''
        Attemps to locate a collection of external systems in the ehb-service database:
        Inputs:
        params is variable length number of dictionaries where each dictionary must include an identifier.
        The allowed identifiers are:
        name = name of the external_system
        url = url of the external system
        example query({"name":"value"},{"url":"value"})
        Returns:
        [dictionaries]
        where each entry is of the form
        {"name":value, "success":True, "externalSystem":[ExternalSystem objects]}
        {"url":value, "success":True, "externalSystem":[ExternalSystem objects]}
        OR
        {"name":value, "success":False, "errors":[error codes]}'''
        body = '['
        for d in params:
            body += '{'
            for k in list(d.keys()):
                v = str(d.get(k))
                if k == 'url':
                    v = ExternalSystem.correctUrl(v)
                body += '"'+k+'":"'+v+'",'
            body = body[0:body.__len__()-1] + '},'
        body = body[0:body.__len__()-1] + ']'
        path = self.root_path + 'query/'
        response = self.processPost(path, body)
        status = []
        for o in json.loads(response):
            errors = o.get("errors", None)
            name = o.get("name", None)
            url = o.get("url", None)
            if errors:
                if url is None:
                    status.append({"name": name, "success": False, "errors": errors})
                else:
                    status.append({"url": url, "success": False, "errors": errors})
            else:
                es = ExternalSystem.identity_from_jsonObject(o.get('externalSystem'))
                if url is None:
                    status.append({"name": name, "success": True, ExternalSystem.identityLabel: es})
                else:
                    status.append({"url": url, "success": True, ExternalSystem.identityLabel: es})

        return status

    def external_records(self, external_system_id, path=None, organization_id=None, subject_id=None):
        '''
        Attempts to get all externalRecord information for the specified externalsystem
        Inputs:
        external_system_id : int value of the externalsystem record id
        path (optional) If specified, this will only return records with this path
        organization_id (optional) : int value of the organization. If specified, this will only return ExternalRecords
                                  whose Subject belongs to this organization
        subject_id (optional) : int value of the subject ehb id. If specified this will only return ExternalRecords
                                belonging to this subject
        Outputs:
        list of ExternalRecord objects
        If no records are found PageNotFound is raised'''
        ehb_service_path = self.root_path + 'id/' + str(external_system_id) + '/'
        if organization_id is None:
            ehb_service_path += 'records/'
        else:
            ehb_service_path += 'organization/' + str(organization_id) + '/records/'
        response = self.processGet(ehb_service_path)
        status = []
        for o in json.loads(response):
            er = ExternalRecord.identity_from_jsonObject(o)
            if path and subject_id:
                if er.subject_id == subject_id and er.path == path:
                        status.append(er)
            elif path:
                if er.path == path:
                    status.append(er)
            elif subject_id:
                if er.subject_id == subject_id:
                    status.append(er)
            else:
                status.append(er)
        if len(status) == 0:
            raise PageNotFound(ehb_service_path)
        else:
            return status

    def subjects(self, external_system_id, path=None, organization_id=None):
        '''
        Attempts to get subject records for subjects that have externalrecords on the specified externalsystem
        Inputs:
        external_system_id : int value of the externalsystem record id
        path (optional) : If specified, this will only return Subjects with externalrecords matching this path
        organization_id (optional) : int value of the organization. If specified, this will only return Subjects
                                  belonging to this organization with externalrecords on the externalsystem
        Outputs:
        list of Subject objects
        If no records are found PageNotFound is raised '''
        ehb_service_path = self.root_path + 'id/' + str(external_system_id) + '/'
        if organization_id is None:
            ehb_service_path += 'subjects/'
        else:
            ehb_service_path += 'organization/' + str(organization_id) + '/subjects/'
        if path:
            ers = self.external_records(external_system_id, path=path, organization_id=organization_id)
        response = self.processGet(ehb_service_path)
        status = []
        for o in json.loads(response):
            s = Subject.identity_from_jsonObject(o)
            if path is None:
                status.append(s)
            else:
                for er in ers:
                    if er.subject_id == s.id and not status.__contains__(s):
                        status.append(s)
        if len(status) == 0:
            raise PageNotFound(ehb_service_path)
        else:
            return status

    def get(self, **id_or_name_or_url):
        id = id_or_name_or_url.pop("id", None)
        if id:
            path = self.root_path + 'id/' + str(id) + '/'
            return ExternalSystem.identity_from_json(self.processGet(path))
        name = id_or_name_or_url.pop('name', None)
        url = id_or_name_or_url.pop('url', None)
        if name or url:
            qry = {}
            if name:
                qry['name'] = name
            else:
                qry['url'] = url
            response = self.query(qry)[0]
            if response.get('success'):
                return response.get(ExternalSystem.identityLabel)
            else:
                msg = self.root_path + ', for get external_system_name = '
                if url is None:
                    msg += name
                else:
                    msg += url
                raise PageNotFound(msg)
        raise InvalidArguments("id, name, or url")

    def delete(self, **id_or_name_or_url):
        id = id_or_name_or_url.pop("id", None)
        if id:
            path = self.root_path + 'id/' + str(id) + '/'
            return self.processDelete(path)
        name = id_or_name_or_url.pop("name", None)
        url = id_or_name_or_url.pop('url', None)
        if name or url:
            qry = {}
            if name:
                qry['name'] = name
            else:
                qry['url'] = url
            es = self.query(qry)[0]
            if es.get("success"):
                id = es.get(ExternalSystem.identityLabel).id
                path = self.root_path + 'id/' + str(id) + '/'
                return self.processDelete(path)
            else:
                msg = self.root_path + ', for delete external_system_name = '
                if url is None:
                    msg += name
                else:
                    msg += url
                raise PageNotFound(msg)
        raise InvalidArguments("id or name")

    def create(self, *externalSystems):
        '''
        Given an arbitrary number of ExternalSystem objects, this method attempts
        to create the externalSystems in the eHB server database.
        '''
        def onSuccess(es, o):
            es.id = int(o.get('id'))
            es.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            es.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        # ensure the urls end in a '/' because Django always does
        for es in externalSystems:
            es.url = ExternalSystem.correctUrl(es.url)
        return self.standardCreate(ExternalSystem, onSuccess, *externalSystems)

    def update(self, *externalSystems):
        '''
        Given an arbitrary number of ExternalSystem objects, this method attempts
        to update the externalsystems in the server database.

        NOTE: It is NOT possible to update the ExternalSystem database id or
        created fields using this method. The modified value will automatically
        be updated in the provided externalsystem objects
        '''
        def onSuccess(es, o):
            es.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        # ensure the urls end in a '/' because Django always does
        for es in externalSystems:
            es.url = ExternalSystem.correctUrl(es.url)
        return self.standardUpdate(ExternalSystem, onSuccess, *externalSystems)
