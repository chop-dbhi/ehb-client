from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
from ehb_client.requests.exceptions import InvalidArguments
import json


class PedigreeRelationship(IdentityBase):
    def __init__(self, subject_1, subject_2, subject_1_role,
                 subject_2_role, protocol_id=None, modified=None, created=None, id=-1):
        self.subject_1 = subject_1
        self.subject_2 = subject_2
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
        print("we are in identity from jsonObject")
        relationships = []
        index = 0
        # because each relationship is represented as two objects we must combine
        # the two objects to collect all relationship details.
        while index < len(jsonObj):
            subject_1 = int(jsonObj[index]['subject_id'])
            subject_2 = int(jsonObj[index]['related_subject_id'])
            # subject_1_role = int(jsonObj[index]['role'])
            # subject_2_role = int(jsonObj[index + 1]['role'])
            subject_1_role = jsonObj[index]['role']
            subject_2_role = jsonObj[index + 1]['role']
            # protocol_id = jsonObj.get('protocol_id') TODO: add protocol in service
            # modified = RequestBase.dateTimeFromJsonString(jsonObj[index]['modified']) TODO: add modified in service
            # created = RequestBase.dateTimeFromJsonString(jsonObj[index]['created']) TODO: add Created in service
            # id = int(jsonObj.get('id')) TODO: add id in service
            index = index + 2
            print("we processed one relationship")
            relationships.append(PedigreeRelationship(subject_1=subject_1,
                                                      subject_2=subject_2,
                                                      subject_1_role=subject_1_role,
                                                      subject_2_role=subject_2_role))

        return relationships

    @staticmethod
    def identity_from_json(pedigreeJsonString):
        print("are we getting to identity from json?")
        print(pedigreeJsonString)
        # for relationship in pedigreeJsonString:
        #     jsonObj = json.loads(relationship)
        jsonObj = json.loads(pedigreeJsonString)
        print("are we getting jsonObj?")
        # TODO: here is the problem
        # does not work
        # relationships = []
        # for pedigree in pedigreeJsonString:
        #     relationships.append(PedigreeRelationship.identity_from_jsonObject(jsonObj))
        #
        # return relationships
        # end does not work
        return PedigreeRelationship.identity_from_jsonObject(jsonObj)

    @staticmethod
    def json_from_identity(pedigree):
        print("are we failing in json from identity")
        print(pedigree)
        # working to get one relationship
        # o = {}
        # o = {
        #     'subject_1': pedigree.subject_1,
        #     'subject_2': pedigree.subject_2,
        #     'subject_1_role': pedigree.subject_1_role,
        #     'subject_2_role': pedigree.subject_2_role,
        #     'protocol_id': pedigree.protocol_id,
        #     'id': pedigree.id
        # }
        # end working to get one relationship

        # TODO: This is the problem - we need to get more than one relationship in this dictionary
        print(type(pedigree))
        if type(pedigree) is list:
            index = 0
            o = []
            for relationship in pedigree:
                o.append({
                    "subject_1": relationship.subject_1,
                    "subject_2": relationship.subject_2,
                    "subject_1_role": relationship.subject_1_role,
                    "subject_2_role": relationship.subject_2_role,
                    "protocol_id": relationship.protocol_id,
                    "id": relationship.id
                })
                index += 1
                print(index)
                print(*o)
                print("we just processed a relationship in json_from_identity")
                print(relationship.subject_2)
        else:
            print("we are not entering else in json from identity")
            o = {}
            o = {
                'subject_1': pedigree.subject_1,
                'subject_2': pedigree.subject_2,
                'subject_1_role': pedigree.subject_1_role,
                'subject_2_role': pedigree.subject_2_role,
                'protocol_id': pedigree.protocol_id,
                'id': pedigree.id
            }


        # Not working
        # o = []
        # for relationship in pedigree:
        #     o.append({
        #         'subject_1': relationship.subject_1,
        #         'subject_2': relationship.subject_2,
        #         'subject_1_role': relationship.subject_1_role,
        #         'subject_2_role': relationship.subject_2_role,
        #         'protocol_id': relationship.protocol_id,
        #         'id': relationship.id
        #     })
        # end not working

        # if pedigree.modified:
        #     o['modified'] = pedigree.modified.strftime('%Y-%m-%d %H:%M:%S.%f')
        # if pedigree.created:
        #     o['created'] = pedigree.created.strftime('%Y-%m-%d %H:%M:%S.%f')
        o.append("this works for some reason")
        print("This is O")
        print(*o)
        # print(json.dumps(pedigree))
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
        # Kinda working but I think we can simplify
        def func(path):
            print("return from ehb get relationship")
            print(PedigreeRelationship.identity_from_json(self.processGet(path)))
            return PedigreeRelationship.identity_from_json(self.processGet(path))
        return self._read_and_action(func, **subid_or_protocolid)
        # end of kinda working





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
