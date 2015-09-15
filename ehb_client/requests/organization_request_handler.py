from ehb_client.requests.base import JsonRequestBase, IdentityBase, RequestBase
import json
from ehb_client.requests.exceptions import InvalidArguments, PageNotFound


class Organization(IdentityBase):

    def __init__(self, name, subject_id_label, modified=None, created=None, id=-1):
        self.name = name
        self.subject_id_label = subject_id_label
        self.modified = modified
        self.created = created
        self.id = id

    @staticmethod
    def findIdentity(searchTermsDict, *identities):
        id = searchTermsDict.get("id", None)
        if id:
            for o in identities:
                if o.id == int(id):
                    return o
        name = searchTermsDict.get("name", None)
        if name:
            for o in identities:
                if o.name == name:
                    return o
        return None

    @staticmethod
    def identity_from_jsonObject(jsonObj):
        name = jsonObj.get('name')
        subj_id_label = jsonObj.get('subject_id_label')
        lm = RequestBase.dateTimeFromJsonString(jsonObj.get('modified'))
        c = RequestBase.dateTimeFromJsonString(jsonObj.get('created'))
        id = int(jsonObj.get('id'))
        return Organization(name=name, subject_id_label=subj_id_label, modified=lm, created=c, id=id)

    @staticmethod
    def identity_from_json(orgJsonString):
        jsonObj = json.loads(orgJsonString)
        return Organization.identity_from_jsonObject(jsonObj)

    @staticmethod
    def json_from_identity(organization):
        q = '"'
        n = '"name":"' + organization.name + q
        sid = '"subject_id_label":"' + organization.subject_id_label + q
        return '{' + n + ',' + sid + '}'

    identityLabel = 'organization'


class OrganizationRequestHandler(JsonRequestBase):

    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, root_path+'/api/organization/', secure, api_key)

    def query(self, *names):
        '''
        Attemps to locate a collection of organization records in the ehb-service database:

        Inputs:
        names : variable length number of organization names to query for
        Returns:
        [dictionaries]
        where each entry is of the form
        {"name":value, "success":True, "organization":[Organization objects]}
        OR
        {"name":value, "success":False, "errors":[error codes]}
        '''
        body = '['
        for n in names:
            body += '{"name":"' + n + '"},'
        body = body[0:body.__len__()-1] + ']'
        path = self.root_path + 'query/'
        response = self.processPost(path, body)
        status = []
        for o in json.loads(response):
            errors = o.get("errors", None)
            name = o.get("name", None)
            if errors:
                status.append({"name": name, "success": False, "errors": errors})
            else:
                org = Organization.identity_from_jsonObject(o.get('organization'))
                status.append({"name": name, "success": True, Organization.identityLabel: org})
        return status

    def _read_and_action(self, path_action, query_action, **id_or_name):
        id = id_or_name.pop("id", None)
        if id:
            path = self.root_path + 'id/' + str(id) + '/'
            return path_action(path)
        name = id_or_name.pop('name', None)
        if name:
            response = self.query(name)[0]
            if response.get('success'):
                return query_action(response.get(Organization.identityLabel))
            else:
                msg = self.root_path + ', for get organization_name = ' + name
                raise PageNotFound(msg)
        raise InvalidArguments("id or name")

    def delete(self, **id_or_name):

        def path_action(path):
            return self.processDelete(path)

        def query_action(org):
            id = org.id
            path = self.root_path + 'id/' + str(id) + '/'
            return self.processDelete(path)

        return self._read_and_action(path_action, query_action, **id_or_name)

    def get(self, **id_or_name):

        def path_action(path):
            return Organization.identity_from_json(self.processGet(path))

        def query_action(org):
            return org

        return self._read_and_action(path_action, query_action, **id_or_name)

    def create(self, *organizations):
        '''
        Given an arbitrary number of Organization objects, this method attempts
        to create the records in the eHB server database.
        '''
        def onSuccess(es, o):
            es.id = int(o.get('id'))
            es.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            es.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardCreate(Organization, onSuccess, *organizations)

    def update(self, *organizations):
        '''
        Given an arbitrary number of Organization objects, this method attempts to update the records in the eHB
        server database. NOTE: It is NOT possible to update the Organization database id or created fields using this
        method. The modified value will automatically be updated in the provided organization objects
        '''
        def onSuccess(es, o):
            es.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardUpdate(Organization, onSuccess, *organizations)
