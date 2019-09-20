from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
from ehb_client.requests.exceptions import InvalidArguments
import json


class SubjFamRelationship(IdentityBase):
    def __init__(self, subject_1_id, subject_2_id, subject_1_role, subject_2_role,
                 protocol_id=None, modified=None, created=None, id=-1, subject_2_org_id=None, subject_1_org_id=None):
        self.subject_1_id = subject_1_id
        self.subject_1_org_id = subject_1_org_id
        self.subject_2_id = subject_2_id
        self.subject_2_org_id = subject_2_org_id
        self.subject_1_role = subject_1_role
        self.subject_2_role = subject_2_role
        self.protocol_id = protocol_id
        self.modified = modified
        self.created = created
        self.id = id

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def findIdentity(searchTermsDict, *identities):
        id = searchTermsDict['id']
        if id:
            for p in identities:
                if p.id == int(id):
                    return p
            return p

    @staticmethod
    def identity_from_jsonObject(jsonObj):
        relationships = []
        # index = 0
        # # because each relationship is represented as two objects we must combine
        # # the two objects to collect all relationship details.
        # while index < len(jsonObj):
        #     subject_1_id = int(jsonObj[index]['subject_id'])
        #     subject_1_org_id = jsonObj[index]['subject_org_id']
        #     subject_2_id = int(jsonObj[index]['related_subject_id'])
        #     subject_2_org_id = jsonObj[index]['related_subject_org_id']
        #     subject_1_role = jsonObj[index]['role']
        #     subject_2_role = jsonObj[index + 1]['role']
        #     id = -1
        #     # protocol_id = jsonObj.get('protocol_id') TODO: add protocol in service
        #     # modified = RequestBase.dateTimeFromJsonString(jsonObj[index]['modified']) TODO: add modified in service
        #     # created = RequestBase.dateTimeFromJsonString(jsonObj[index]['created']) TODO: add Created in service
        #     # id = int(jsonObj.get('id')) TODO: add id in service
        #     index = index + 2
        #     relationships.append(subjFamRelationship(subject_1_id=subject_1_id,
        #                                               subject_1_org_id=subject_1_org_id,
        #                                               subject_2_id=subject_2_id,
        #                                               subject_2_org_id=subject_2_org_id,
        #                                               subject_1_role=subject_1_role,
        #                                               subject_2_role=subject_2_role,
        #                                               id=id)),

        for item in jsonObj:
            relationships.append(SubjFamRelationship(subject_1_id=int(item['subject_1']['id']),
                                                          subject_1_org_id=item['subject_1']['organization_subject_id'],
                                                          subject_2_id=int(item['subject_2']['id']),
                                                          subject_2_org_id=item['subject_2']['organization_subject_id'],
                                                          subject_1_role=item['subject_1_role']['desc'],
                                                          subject_2_role=item['subject_2_role']['desc'],
                                                          id=item['id']))

        return relationships

    @staticmethod
    def identity_from_json(subjFamJsonString):
        jsonObj = json.loads(subjFamJsonString)
        return SubjFamRelationship.identity_from_jsonObject(jsonObj)

    @staticmethod
    def json_from_identity(subjFam):
        if type(subjFam) is list:
            o = []
            for relationship in subjFam:
                o.append({
                    "subject_1_id": relationship.subject_1_id,
                    "subject_1_org_id": relationship.subject_1_org_id,
                    "subject_2_id": relationship.subject_2_id,
                    "subject_2_org_id": relationship.subject_2_org_id,
                    "subject_1_role": relationship.subject_1_role,
                    "subject_2_role": relationship.subject_2_role,
                    "protocol_id": relationship.protocol_id,
                    "id": relationship.id
                })
        else:
            o = {}
            o = {
                'subject_1': subjFam.subject_1_id,
                'subject_2': subjFam.subject_2_id,
                'subject_1_role': subjFam.subject_1_role,
                'subject_2_role': subjFam.subject_2_role,
                'protocol_id': subjFam.protocol_id,
                'id': subjFam.id
            }
        return json.dumps(o)

    identityLabel = "subjFamRelationship"


class SubjFamRelationshipRequestHandeler(JsonRequestBase):
    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, '{0}/api/famRelation/'.format(root_path), secure, api_key)

    def _read_and_action(self, func, **id):
        subject_id = id.pop('subject_id', None)
        protocol_id = id.pop('protocol_id', None)
        relationship_id = id.pop('relationship_id', None)
        if subject_id:
            path = self.root_path + 'subject_id/' + str(subject_id) + '/'
            return func(path)
        if protocol_id:
            path = self.root_path + 'protocol_id/' + str(protocol_id) + '/'
            return func(path)
        if relationship_id:
            path = self.root_path + 'relationship_id/' + str(relationship_id) + '/'
            return func(path)
        raise InvalidArguments("subject id, protocol id or relationship id required")

    def get(self, **id):
        '''
        Given a id = subject id integer
        OR protocol_id = string
        this method polls the server for the relationships.
        '''
        def func(path):
            return SubjFamRelationship.identity_from_json(self.processGet(path))
        return self._read_and_action(func, **id)

    def create(self, *relationships):
        def onSuccess(p, o):
            p.id = int(o['id'])
            # TODO getting created and modified cause NoneType error
            # p.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            # p.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardCreate(SubjFamRelationship, onSuccess, *relationships)

    def update(self, *relationships):
        def onSuccess(relationship, o):
            relationship.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardUpdate(SubjFamRelationship, onSuccess, *relationships)

    def delete(self, **relationship_id):
        def func(path):
            return self.processDelete(path)
        return self._read_and_action(func, **relationship_id)


class RelationshipTypeRequestHandler(JsonRequestBase):
    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, '{0}/api/famRelation/relationship_types'.format(root_path), secure, api_key)

    def get(self):
        path = self.root_path + '/api/famRelation/relationship_types/'
        return self.processGet(path)

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
