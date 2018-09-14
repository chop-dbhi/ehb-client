from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
from ehb_client.requests.request_handler import RequestHandler
import json
from ehb_client.requests.exceptions import PageNotFound, InvalidArguments

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


class PedigreeRelationshipRequestHandeler(JsonRequestBase):
    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, '{0}/api/pedigree/'.format(root_path), secure, api_key)

    def get(self, **kwargs):
        pass

    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
