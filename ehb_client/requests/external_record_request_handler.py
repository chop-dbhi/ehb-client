from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
from ehb_client.requests.request_handler import RequestHandler
import json
from ehb_client.requests.exceptions import PageNotFound, InvalidArguments


class ExternalRecord(IdentityBase):

    def __init__(self, record_id, subject_id=-1, external_system_id=-1,
                 path='', modified=None, created=None, id=-1, label_id=1):
        self.record_id = record_id
        self.subject_id = subject_id  # this is the id of the ehb-service Subject record id
        self.external_system_id = external_system_id
        self.modified = modified
        self.created = created
        self.path = path
        self.id = id
        self.label_id = label_id

    @staticmethod
    def findIdentity(searchTermsDict, *identities):
        id = searchTermsDict.get("id", None)
        path = searchTermsDict.get('path', None)
        record_id = searchTermsDict.get('record_id')
        if id:
            for s in identities:
                if s.id == int(id):
                    return s
        if record_id:
            if path:
                for s in identities:
                    if s.record_id == record_id and s.path == path:
                        return s
            else:
                for s in identities:
                    if s.record_id == record_id:
                        return s
        return None

    @staticmethod
    def identity_from_json(erJsonString):
        jsonObj = json.loads(erJsonString)
        return ExternalRecord.identity_from_jsonObject(jsonObj)

    @staticmethod
    def identity_from_jsonObject(jsonObj):
        es_id = int(jsonObj.get('external_system_id'))
        s_id = int(jsonObj.get('subject_id'))
        lm = RequestBase.dateTimeFromJsonString(jsonObj.get('modified'))
        c = RequestBase.dateTimeFromJsonString(jsonObj.get('created'))
        id = int(jsonObj.get('id'))
        rec_id = jsonObj.get('record_id')
        p = jsonObj.get('path')
        lbl = jsonObj.get('label_id')
        return ExternalRecord(
            record_id=rec_id,
            external_system_id=es_id,
            subject_id=s_id,
            path=p,
            modified=lm,
            created=c,
            id=id,
            label_id=lbl
        )

    @staticmethod
    def json_from_identity(er):
        q = '"'
        s = '"subject":"' + str(er.subject_id) + q
        es = '"external_system":"' + str(er.external_system_id) + q
        rec = '"record_id":"' + er.record_id + q
        p = '"path":"' + er.path + q
        if er.label_id:
            rel = '"label":"' + str(er.label_id) + q
        else:
            rel = '"label":"' + 'null' + q
        return '{' + s + ',' + es + ',' + rec + ',' + p + ',' + rel + '}'

    identityLabel = "external_record"


class ExternalRecordRequestHandler(JsonRequestBase):

    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, root_path+'/api/externalrecord/', secure, api_key)

    def query(self, *params):
        '''Attemps to locate a collection of external records in the ehb-service database:
        Inputs:
        params is variable length number of dictionaries where each dictionary includes one or more sets of
        identifiers. The query can be on any combination of Subject, ExternalSystem and path.
        It is not necessary to specify all 3, but at least 1 must be provided.
        -The allowed ExternalSystem identifiers are:
        external_system_id = integer value of the external_system id
        OR
        external_system_name = string value of the external_systyem name
        OR
        external_system_url = string value of the external_system URL
        -The allowed Subject identifiers are:
        subject_id = integer value of the subject id
        OR
        subject_org = int value of the eHB Organization record id for this subject
        subject_org_id = string value of the organization_subject_id for this Subject
        -The allowed path identifier is path
        example query({"subject_id":1, "external_system_id":2, "path":"thepath"},{"subject_id":2, "external_system_name":"somename"})
        Returns:
        [dictionaries]
        where each entry is of the form
        {"external_system":value, "subject":"id":"value", "success":boolean, "external_record":[ExternalRecords objects]}
        {"external_system":value, "subject":{"subject_org":"value", "subject_org_id":"value"}, "success":boolean, "external_record":[ExternalRecords objects]}
        OR
        {"external_system":value, "subject":value, "success":boolean, "errors":[error codes]}'''
        body = '['
        for d in params:
            body += '{'
            for k in d.keys():
                body += '"'+k+'":"'+str(d.get(k))+'",'
            body = body[0:body.__len__()-1] + '},'
        body = body[0:body.__len__()-1] + ']'
        path = self.root_path + 'query/'
        response = self.processPost(path, body)
        status = []
        for o in json.loads(response):
            errors = o.get("errors", None)
            es = o.get('external_system', o.get('external_system_id', o.get('external_system_url', 'not_provided')))
            s = o.get('subject_id', 'not_provided')
            if s == 'not_provided':
                s_org = o.get('subject_org', None)
                s_org_id = o.get('subject_org_id', None)
                if s_org and s_org_id:
                    s = {
                        'subject_org': o.get('subject_org'),
                        'subject_org_id': o.get('subject_org_id')
                    }
            path = o.get('path', 'not_provided')
            if errors:
                status.append({"external_system":es, "path":path, "subject":s, "success":False, "errors":errors})
            else:
                ers = o.get('external_record')
                era = []
                for er in ers:
                    era.append(ExternalRecord.identity_from_jsonObject(er))
                status.append({"external_system":es, "path":path, "subject":s, "success":True, ExternalRecord.identityLabel:era})
        return status

    def __processAfterQueryOnKwargs(self, f_found, f_notfound, **kwargs):
        subject_id = kwargs.pop('subject_id',None)
        subject_org = kwargs.pop('subject_org', None)
        subject_org_id = kwargs.pop('subject_org_id', None)
        es_id = kwargs.pop('external_system_id', None)
        es_name = kwargs.pop('external_system_name', None)
        es_url = kwargs.pop('external_system_url', None)
        path = kwargs.pop('path', None)
        label_id = kwargs.pop('label_id', None)

        qdict = {}
        subfound = False
        esfound = False
        pathFound = False
        if subject_id:
            qdict['subject_id'] = subject_id
            subfound = True
        if subject_org and subject_org_id:
            qdict['subject_org'] = subject_org
            qdict['subject_org_id'] = subject_org_id
            subfound = True
        if es_id:
            qdict['external_system_id'] = es_id
            esfound = True
        if es_name:
            qdict['external_system_name'] = es_name
            esfound = True
        if es_url:
            qdict['external_system_url'] = es_url
            esfound = True
        if path:
            qdict['path'] = path
            pathFound = True
        if label_id:
            qdict['label_id'] = label_id
        if esfound or subfound or pathFound:
            return f_found(self.query(qdict), qdict)
        else:
            return f_notfound(qdict)

    def get(self, **kwargs):
        '''Attempts to locate the external record in the ehb-service database:
        Inputs:
            id = integer value of the externalRecord record id in the ehb-service
        OR any combination of Subject, ExternalSystem and path. In this case it is not possible to
        guarantee a single value in the response.
        It is not necessary to specify all 3, but at least 1 must be provided.
        -The allowed ExternalSystem identifiers are:
        external_system_id = integer value of the external_system id
        OR
        external_system_name = string value of the external_systyem name
        OR
        external_system_url = string value of external_system URL
        -The allowed Subject identifiers are:
        subject_id = integer value of the ehb subject id
        OR
        subject_org = int value of the eHB Organization record id for this subject
        subject_org_id = string value of the organization_subject_id for this Subject
        -The allowed path identifier is path
        Output:
        A list of ExternalRecord objects'''
        rid = kwargs.pop('id', None)

        if rid:
            path = self.root_path + 'id/' + str(rid) + '/'
            return ExternalRecord.identity_from_json(self.processGet(path))
        else:
            def onProperKw(query_response, qdict):
                response = query_response[0]
                if response.get('success'):
                    return response.get(ExternalRecord.identityLabel)
                else:
                    msg = self.root_path + ', for get by ' + str(qdict)
                    raise PageNotFound(msg)

            def onImproperKw(qdict):
                msg = 'external_system_id OR external_system_name AND subject_id OR subject_org AND subject_org_id'
                raise InvalidArguments(msg)

            return self.__processAfterQueryOnKwargs(onProperKw, onImproperKw, **kwargs)

    def delete(self, **kwargs):
        '''Attempts to delete the external record in the ehb-service database:
        Inputs:
            id = integer value of the externalRecord record id in the ehb-service
        OR any combination of Subject, ExternalSystem and path.
        It is not necessary to specify all 3, but at least 1 must be provided.
        -The allowed ExternalSystem identifiers are:
        external_system_id = integer value of the external_system id
        OR
        external_system_name = string value of the external_systyem name
        OR
        external_system_url = string value of external_system URL
        -The allowed Subject identifiers are:
        subject_id = integer value of the subject id
        OR
        subject_org = int value of the eHB Organization record id for this subject
        subject_org_id = string value of the organization_subject_id for this Subject
        -The allowed path identifier is path
        **WARNING**: If multiple externalRecords are found for the specified values they will all be deleted.
        If this is not the desired behavior it is recommended to only allow deleting by id'''
        id = kwargs.pop('id', None)
        if id:
            path = self.root_path + 'id/' + str(id) + '/'
            return self.processDelete(path)
        else:
            def onProperKw(query_response, qdict):
                response = query_response[0]
                if response.get('success'):
                    for er in response.get(ExternalRecord.identityLabel):
                        id = er.id
                        path = self.root_path + 'id/' + str(id) + '/'
                        self.processDelete(path)
                else:
                    msg = self.root_path + ', for delete external_record by ' + str(qdict)
                    raise PageNotFound(msg)

            def onImproperKw(qdict):
                msg = 'external_system_id OR external_system_name AND subject_id OR subject_mrn'
                raise InvalidArguments(msg)

            return self.__processAfterQueryOnKwargs(onProperKw, onImproperKw, **kwargs)

    def create(self, *externalRecords):
        '''Given an arbitrary number of ExternalRecord objects, this method attempts to create the externalRecords
        in the server database.'''
        def onSuccess(er, o):
            er.id = int(o.get('id'))
            er.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            er.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardCreate(ExternalRecord, onSuccess, *externalRecords)

    def update(self, *externalRecords):
        '''Given an arbitrary number of ExternalRecord objects, this method attempts to update the externalrecords in the
        server database. NOTE: It is NOT possible to update the ExternalRecord database id or created fields using this
        method. The modified value will automatically be updated in the provided externalrecord objects'''
        def onSuccess(er, o):
            er.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardUpdate(ExternalRecord, onSuccess, *externalRecords)

class ExternalRecordLabelRequestHandler(RequestHandler):
    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestHandler.__init__(self, host, secure, api_key)
        self.root_path = root_path

    def get(self, **kwargs):
        lid = kwargs.pop('id', None)
        path = self.root_path + '/api/externalrecord/labels/{0}/'.format(lid)
        response = self.sendRequest('GET', path, {'Content-Type': 'application/json'})
        try:
            return json.loads(response.read())
        except:
            return None

    def query(self, *params):
        path = self.root_path + '/api/externalrecord/labels/'
        response = self.sendRequest('POST', path, {'Content-Type': 'application/json'})

        return json.loads(response.read())
