from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
from ehb_client.requests.exceptions import InvalidArguments
import json


class PedigreeRelationship(IdentityBase):
    def __init__(self, subject_1_id, subject_1_org_id, subject_2_id, subject_2_org_id, subject_1_role,
                 subject_2_role, protocol_id=None, modified=None, created=None, id=-1):
        self.subject_1_id = subject_1_id
        self.subject_1_org_id = subject_1_org_id
        self.subject_2 = subject_2_id
        self.subject_2_org_id = subject_2_org_id
        self.subject_1_role = subject_1_role
        self.subject_2_role = subject_2_role
        self.protocol_id = protocol_id
        self.modified = modified
        self.created = created
        self.id = id

    @staticmethod
    def findIdentity(searchTermsDict, *identities):
        id = searchTermsDict.get("id", None)
        if id:
            for p in identities:
                if p.id == int(id):
                    return p

    @staticmethod
    def identity_from_jsonObject(jsonObj):
        relationships = []
        index = 0
        # because each relationship is represented as two objects we must combine
        # the two objects to collect all relationship details.
        while index < len(jsonObj):
            subject_1_id = int(jsonObj[index]['subject_id'])
            subject_1_org_id = jsonObj[index]['subject_org_id']
            subject_2_id = int(jsonObj[index]['related_subject_id'])
            subject_2_org_id = jsonObj[index]['related_subject_org_id']
            subject_1_role = jsonObj[index]['role']
            subject_2_role = jsonObj[index + 1]['role']
            id = -1
            # protocol_id = jsonObj.get('protocol_id') TODO: add protocol in service
            # modified = RequestBase.dateTimeFromJsonString(jsonObj[index]['modified']) TODO: add modified in service
            # created = RequestBase.dateTimeFromJsonString(jsonObj[index]['created']) TODO: add Created in service
            # id = int(jsonObj.get('id')) TODO: add id in service
            index = index + 2
            relationships.append(PedigreeRelationship(subject_1_id=subject_1_id,
                                                      subject_1_org_id=subject_1_org_id,
                                                      subject_2_id=subject_2_id,
                                                      subject_2_org_id=subject_2_org_id,
                                                      subject_1_role=subject_1_role,
                                                      subject_2_role=subject_2_role,
                                                      id=id)),

        return relationships

    @staticmethod
    def identity_from_json(pedigreeJsonString):
        jsonObj = json.loads(pedigreeJsonString)
        return PedigreeRelationship.identity_from_jsonObject(jsonObj)

    @staticmethod
    def json_from_identity(pedigree):
        if type(pedigree) is list:
            o = []
            for relationship in pedigree:
                o.append({
                    "subject_1_id": relationship.subject_1_id,
                    "subject_1_org_id": relationship.subject_1_org_id,
                    "subject_2_id": relationship.subject_2,
                    "subject_2_org_id": relationship.subject_2_org_id,
                    "subject_1_role": relationship.subject_1_role,
                    "subject_2_role": relationship.subject_2_role,
                    "protocol_id": relationship.protocol_id,
                    "id": relationship.id
                })
        else:
            o = {}
            o = {
                'subject_1': pedigree.subject_1,
                'subject_2': pedigree.subject_2,
                'subject_1_role': pedigree.subject_1_role,
                'subject_2_role': pedigree.subject_2_role,
                'protocol_id': pedigree.protocol_id,
                'id': pedigree.id
            }
        return json.dumps(o)

    identityLabel = "pedigreeRelationship"


class PedigreeRelationshipRequestHandeler(JsonRequestBase):
    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, '{0}/api/pedigree/'.format(root_path), secure, api_key)

    def _read_and_action(self, func, **subid_or_protocolid):
        subject_id = subid_or_protocolid.pop('subject_id', None)
        protocol_id = subid_or_protocolid.pop('protocol_id', None)
        if subject_id:
            path = self.root_path + 'subject_id/' + str(subject_id) + '/'
            return func(path)
        if protocol_id:
            path = self.root_path + 'protocol_id/' + str(protocol_id) + '/'
            return func(path)
        raise InvalidArguments("subject id or protocol id required")

    def get(self, **subid_or_protocolid):
        '''
        Given a id = subject id integer
        OR protocol_id = string
        this method polls the server for the relationships.
        '''
        def func(path):
            return PedigreeRelationship.identity_from_json(self.processGet(path))
        return self._read_and_action(func, **subid_or_protocolid)

    def create(self, *relationships):
        def onSuccess(p, o):
            # TODO getting created and modified cause NoneType error
            # p.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            # p.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
            pass
        return self.standardCreate(PedigreeRelationship, onSuccess, *relationships)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
