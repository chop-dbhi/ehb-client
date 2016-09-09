from ehb_client.requests.base import JsonRequestBase, IdentityBase, RequestBase
import json
from ehb_client.requests.exceptions import InvalidArguments


class Subject(IdentityBase):

    def __init__(self, first_name=None, last_name=None, organization_id=-1,
                 organization_subject_id=-1, dob=-1, modified=None, created=None, id=-1):
        self.first_name = first_name
        self.last_name = last_name
        self.organization_id = organization_id  # eHB id of the associated Organization object
        self.organization_subject_id = organization_subject_id  # id used by the Organization for this subject
        self.dob = dob
        self.modified = modified
        self.created = created
        self.id = id  # the eHB id for this Subject object

    @staticmethod
    def findIdentity(searchTermsDict, *identities):
        id = searchTermsDict.get("id", None)
        if id:
            for s in identities:
                if s.id == int(id):
                    return s
        org_id = searchTermsDict.get("organization_id", None)
        org_subj_id = searchTermsDict.get('organization_subject_id', None)
        if org_id and org_subj_id:
            for s in identities:
                if s.organization_id == int(org_id) and s.organization_subject_id == org_subj_id:
                    return s
        return None

    @staticmethod
    def identity_from_jsonObject(jsonObj):
        fn = jsonObj.get('first_name')
        ln = jsonObj.get('last_name')
        org_id = int(jsonObj.get('organization'))
        org_subj_id = jsonObj.get('organization_subject_id')
        dob = RequestBase.dateFromString(jsonObj.get('dob'))
        lm = RequestBase.dateTimeFromJsonString(jsonObj.get('modified'))
        c = RequestBase.dateTimeFromJsonString(jsonObj.get('created'))
        id = int(jsonObj.get('id'))
        return Subject(first_name=fn, last_name=ln, organization_id=org_id,
                       organization_subject_id=org_subj_id, dob=dob,
                       modified=lm, created=c, id=id)

    @staticmethod
    def identity_from_json(subjectJsonString):
        jsonObj = json.loads(subjectJsonString)
        return Subject.identity_from_jsonObject(jsonObj)

    @staticmethod
    def json_from_identity(subject):
        if not hasattr(subject, 'group_name'):
            subject.group_name = ''
        o = {}
        o = {
            'first_name': subject.first_name,
            'last_name': subject.last_name,
            'group_name': subject.group_name,
            'organization_subject_id': subject.organization_subject_id,
            'organization': subject.organization_id,
            'dob': RequestBase.stringFromDate(subject.dob),
            'id': subject.id
        }

        if subject.modified:
            o['modified'] = subject.modified.strftime('%Y-%m-%d %H:%M:%S.%f')
        if subject.created:
            o['created'] = subject.created.strftime('%Y-%m-%d %H:%M:%S.%f')

        return json.dumps(o)

    identityLabel = "subject"


class SubjectRequestHandler(JsonRequestBase):

    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, root_path+'/api/subject/', secure, api_key)

    def _read_and_action(self, func, **id_or_orgInfo):
        pk = id_or_orgInfo.pop("id", None)
        if pk:
            path = self.root_path + 'id/' + str(pk) + '/'
            return func(path)
        org_id = id_or_orgInfo.pop('organization_id', None)
        org_subj_id = id_or_orgInfo.pop('organization_subject_id', None)
        if org_id and org_subj_id:
            path = self.root_path + 'organization/' + str(org_id) + '/osid/' + org_subj_id + '/'
            return func(path)
        raise InvalidArguments("id OR organization_id AND organization_subject_id")

    def standardUpdate(self, identityBase, successFunc, *identities):
        '''
        Given an arbitrary number of Identity objects of type X(IdentityBase),
        this method attempts to updated the identity objects in the server database.
        Inputs:
            identityBase: The Class object that extends IdentityBase
            successFunc: a function that accepts an object, i, of type identityBase
                and a dictionary of values that can be used to populate i.
                Typically these will be values provided by the server after
                creation, e.g. created date. The return value of this function
                is not used
            identities: the identity objects to be loaded from to the server
        Output:
          list of dictionaries :
            {identityBase.identityLabel:identity object, "success":boolean, "errors":errors}
            where errors is None if there were no errors in creating the object
            in the server db
        '''
        path = self.root_path
        body = '['
        for i in identities:
            id = i.id
            old_subject = identityBase.json_from_identity(i.old_subject)
            new_subject = identityBase.json_from_identity(i)
            body += '{"id":"'+str(id)+'","old_subject":'+old_subject+',"new_subject":'+new_subject+'},'
        body = body[0:body.__len__()-1] + ']'
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

    def get(self, **id_or_orgInfo):
        '''
        Given a id = subject id integer
        OR organization_id = Organization id int AND organization_subject_id = string
        this method polls the server for the Subject. If found returns a Subject object
        '''
        def func(path):
            return Subject.identity_from_json(self.processGet(path))
        return self._read_and_action(func, **id_or_orgInfo)

    def delete(self, **id_or_orgInfo):
        '''
        Given a id = subject id integer or mrn = subject mrn string, this method
        polls the server to delete the Subject. Returns the empty response if
        successful, raises an exception otherwise
        '''
        def func(path):
            return self.processDelete(path)
        return self._read_and_action(func, **id_or_orgInfo)

    def create(self, *subjects):
        '''
        Given an arbitrary number of Subject objects, this method attempts to
        create the subjects in the server database.
        '''
        def onSuccess(s, o):
            s.id = int(o.get('id'))
            s.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            s.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardCreate(Subject, onSuccess, *subjects)

    def update(self, *subjects):
        '''
        Given an arbitrary number of Subject objects, this method attempts to
        update the subjects in the server database.
        NOTE: It is NOT possible to update the Subject database id or created
        fields using this method. The modified value will automatically be
        updated in the provided subject objects
        '''
        def onSuccess(s, o):
            s.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardUpdate(Subject, onSuccess, *subjects)
