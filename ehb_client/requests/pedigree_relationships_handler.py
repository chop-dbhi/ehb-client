from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
from ehb_client.requests.exceptions import InvalidArguments
import json
# from ehb_client.requests.request_handler import RequestHandler
# import json
# from ehb_client.requests.exceptions import PageNotFound, InvalidArguments


class PedigreeRelationship(IdentityBase):
    def __init__(self, subject_1, subject_2, subject_1_role,
                 subject_2_role, protocol_id, modified=None, created=None, id=-1):
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
        pass

    @staticmethod
    def identity_from_json(pedigreeJsonString):
        pass

    @staticmethod
    def json_from_identity(pedigree):

        o = {}
        o = {
            'subject_1': pedigree.subject_1,
            'subject_2': pedigree.subject_2,
            'subject_1_role': pedigree.subject_1_role,
            'subject_2_role': pedigree.subject_2_role,
            'protocol_id': pedigree.protocol_id,
            'id': pedigree.id
        }

        if pedigree.modified:
            o['modified'] = pedigree.modified.strftime('%Y-%m-%d %H:%M:%S.%f')
        if pedigree.created:
            o['created'] = pedigree.created.strftime('%Y-%m-%d %H:%M:%S.%f')

        return json.dumps(o)

    identityLabel = "PedigreeRelationship"


class PedigreeRelationshipRequestHandeler(JsonRequestBase):
    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, '{0}/api/pedigree/'.format(root_path), secure, api_key)

    # TODO update this for relationships - used to get added elements needed for URL request
    # def _read_and_action(self, func, **sub_id_or_protocol_id):
    #     pk = sub_id_or_protocol_id.pop("id", None)
    #     if pk:
    #         path = self.root_path + 'id/' + str(pk) + '/'
    #         return func(path)
    #     org_id = sub_id_or_protocol_id.pop('organization_id', None)
    #     org_subj_id = sub_id_or_protocol_id.pop('organization_subject_id', None)
    #     if org_id and org_subj_id:
    #         path = self.root_path + 'organization/' + str(org_id) + '/osid/' + org_subj_id + '/'
    #         return func(path)
    #     raise InvalidArguments("id OR organization_id AND organization_subject_id")

    def get(self, **kwargs):
        pass

    def create(self, *relationships):
        def onSuccess(p, o):
            # er.id = int(o.get('id'))
            p.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            p.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardCreate(PedigreeRelationship, onSuccess, *relationships)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
