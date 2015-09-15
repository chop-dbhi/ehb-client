from ehb_client.requests.base import JsonRequestBase, RequestBase, IdentityBase
import json
from ehb_client.requests.exceptions import PageNotFound, InvalidArguments
from ehb_client.requests.subject_request_handler import Subject
from ehb_client.requests.external_record_request_handler import ExternalRecord


class Group(IdentityBase):

    def __init__(self, name, description, is_locking, client_key, ehb_key=None,
                 modified=None, created=None, id=-1):
        '''
        Represents a Group in the eHB system. Note that client_key is NEVER
        provided by a response as the eHB only stores salted and hashed versions
        of client_key. A value of client_key should be provided when

        1. creating a new Group (required)
        2. updating an existing Group (optional, not needed if keeping existing client_key)

        When updating a Group using the request handler's update method it is
        necessary to have called the 'current_client_key' method on this Group
        '''
        self.name = name
        self.description = description
        self.is_locking = is_locking
        self.client_key = client_key
        self.ehb_key = ehb_key
        self.modified = modified
        self.created = created
        self._current_client_key = None
        self.id = id

    def current_client_key(self, key): self._current_client_key = key

    @staticmethod
    def findIdentity(searchTermsDict, *identities):
        gid = searchTermsDict.get('id')
        if gid:
            for grp in identities:
                if grp.id == int(gid):
                    return grp
        gname = searchTermsDict.get('name')
        if gname:
            for grp in identities:
                if grp.name == gname:
                    return grp

    identityLabel = 'group'

    @staticmethod
    def identity_from_json(groupJsonString):
        return Group.identity_from_jsonObject(json.loads(groupJsonString))

    @staticmethod
    def identity_from_jsonObject(jsonObj):
        n = jsonObj.get('name')
        des = jsonObj.get('description')
        lm = RequestBase.dateTimeFromJsonString(jsonObj.get('modified'))
        c = RequestBase.dateTimeFromJsonString(jsonObj.get('created'))
        gid = int(jsonObj.get('id'))
        il = jsonObj.get('is_locking', 'false').lower() == 'true'
        ek = jsonObj.get('ehb_key')
        ck = None
        return Group(name=n, description=des, is_locking=il, ehb_key=ek,
                     client_key=ck, modified=lm, created=c, id=gid)

    @staticmethod
    def json_from_identity(grp):
        q = '"'
        c = ','
        n = '"name":"' + grp.name + q
        des = '"description":"' + grp.description + q
        il = '"is_locking":' + str(grp.is_locking).lower()
        ck = '"client_key":"' + grp.client_key + q
        body = '{' + n + c + des + c + il + c + ck
        if grp._current_client_key:
            body += c + '"current_client_key":"' + grp._current_client_key + q
        body += '}'
        return body


class GroupRequestHandler(JsonRequestBase):

    def __init__(self, host, root_path='', secure=False, api_key=None):
        RequestBase.__init__(self, host, root_path+'/api/group/', secure, api_key)

    def _process_by_id_or_name(self, func, **id_or_name):
        gid = id_or_name.pop('id', None)
        if gid:
            path = self.root_path + '?id=' + str(gid)
            return func(path)
        gname = id_or_name.pop('name', None)
        if gname:
            path = self.root_path + '?name=' + gname
            return func(path)
        raise InvalidArguments('id OR name')

    def get(self, **id_or_name):
        def func(path):
            return Group.identity_from_json(self.processGet(path))
        return self._process_by_id_or_name(func, **id_or_name)

    def get_subjects(self, group):
        '''
        Attempts to get all the subjects, if any associated with this group
        '''
        return self._get_x_in_group(group, Subject, '/subjects/')

    def add_subjects(self, group, subjects):
        '''
        Attempts to add each subject to the group. These subjects must already be in the eHB
        '''
        return self._add_x_to_group(group, Subject, '/subjects/', subjects)

    def remove_subject(self, group, subject):
        '''
        Attempts to remove subject from the group. The subject must already be in the eHB
        '''
        return self._remove_x_from_group(group, '/subjects/', subject)

    def get_records(self, group):
        '''
        Attempts to get all the externalRecords, if any assoicated with this group
        '''
        return self._get_x_in_group(group, ExternalRecord, '/records/')

    def add_records(self, group, external_records):
        '''
        Attempts to add each record to the group. These records must already be in the eHB
        '''
        return self._add_x_to_group(group, ExternalRecord, '/records/', external_records)

    def remove_record(self, group, external_record):
        '''
        Attempts to remove external_record from the group. The ExternalRecord must arleady be in the eHB
        '''
        return self._remove_x_from_group(group, '/records/', external_record)

    def _add_x_to_group(self, group, X, xpath, xs):
        '''
        Attempts to add each x from x of type X to the group. These xs must already be in the eHB
        '''
        ehb_service_path = self.root_path + 'id/' + str(group.id) + xpath
        headers = {'Content-Type': 'application/json'}
        if group.is_locking:
            headers = {'GROUP-CLIENT-KEY': group.client_key, 'Content-Type': 'application/json'}
        body = '['
        for x in xs:
            body += str(x.id) + ','
        body = body[0:len(body)-1] + ']'
        response = self.processPost(ehb_service_path, body, headers)
        return json.loads(response)

    def _get_x_in_group(self, group, X, xpath):
        '''
        Attempts to get objects of type x, if any, associated with this group
        '''
        ehb_service_path = self.root_path + 'id/' + str(group.id) + xpath
        headers = {'Accept': 'application/json'}
        if group.is_locking:
            headers = {'GROUP-CLIENT-KEY': group.client_key, 'Accept': 'application/json'}
        response = self.processGet(ehb_service_path, headers)
        return [X.identity_from_jsonObject(o) for o in json.loads(response)]

    def _remove_x_from_group(self, group, xpath, x):
        '''
        Attempts to remove x of type X from the group. The x must already be in the eHB
        '''
        ehb_service_path = self.root_path + 'id/' + str(group.id) + xpath + 'id/' + str(x.id) + '/'
        headers = {'Accept': 'application/json'}
        if group.is_locking:
            headers = {'GROUP-CLIENT-KEY': group.client_key, 'Accept': 'application/json'}
        return self.processDelete(ehb_service_path, headers)

    def delete(self, **kwargs):
        '''
        Delete a Group. kwargs MUST include the following:
        client_key : current value of the Group's client_key
        id : the Group's id
        OR
        name : the Group's name
        '''
        cck = kwargs.get('client_key')
        if not cck:
            raise InvalidArguments('client_key')

        def func(path):
            return self.processDelete(path, {'GROUP-CLIENT-KEY': cck, 'Accept': 'application/json'})

        return self._process_by_id_or_name(func, **kwargs)

    def create(self, *groups):
        '''
        Given an arbitrary number of Group objects, this method attempts to
        create the groups in the eHB server database.
        '''

        def onSuccess(grp, o):
            grp.id = int(o.get('id'))
            grp.created = RequestBase.dateTimeFromJsonString(o.get('created'))
            grp.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
            grp.ehb_key = o.get('ehb_key')
        return self.standardCreate(Group, onSuccess, *groups)

    def update(self, *groups):
        '''
        This method will fail if 'current_client_key' method has not been
        called on each Group.
        If successful this method will update the current_client_key to the
        value of client_key
        '''
        def onSuccess(g, o):
            g.current_client_key(g.client_key)
            g.modified = RequestBase.dateTimeFromJsonString(o.get('modified'))
        return self.standardUpdate(Group, onSuccess, *groups)
