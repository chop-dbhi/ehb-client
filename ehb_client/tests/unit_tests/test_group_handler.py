import pytest
import json
import datetime
from ehb_client.requests.group_request_handler import Group, \
    GroupRequestHandler
from ehb_client.requests.group_request_handler import Subject
from ehb_client.requests.external_record_request_handler import ExternalRecord
from ehb_client.requests import exceptions


@pytest.fixture(scope='module')
def handler():
    return GroupRequestHandler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return GroupRequestHandler(
        host='example.com',
        root_path='',
        secure=True,
        api_key='testkey'
    )


def test_handler_initialization(handler):
    assert handler.host == 'example.com'
    assert handler.root_path == '/api/group/'
    assert not handler.secure
    assert handler.request_handler.api_key == 'testkey'


def test_secure_handler_initialization(secure_handler):
    assert secure_handler.host == 'example.com'
    assert secure_handler.root_path == '/api/group/'
    assert secure_handler.secure
    assert secure_handler.request_handler.api_key == 'testkey'


def test_identity_to_json():
    group = Group(
        id=1,
        name='TestGroup',
        description='A test group',
        is_locking=True,
        client_key='testclientkey',
        ehb_key='testehbkey',
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1),
    )
    jsonStr = group.json_from_identity(group)
    assert isinstance(jsonStr, str)
    assert json.loads(jsonStr)


def test_identity_to_json_setck():
    group = Group(
        id=1,
        name='TestGroup',
        description='A test group',
        is_locking=True,
        client_key='testclientkey',
        ehb_key='testehbkey',
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1),
    )
    group.current_client_key('newck')
    jsonStr = group.json_from_identity(group)
    assert isinstance(jsonStr, str)
    Obj = json.loads(jsonStr)
    assert isinstance(Obj, dict)
    assert Obj['current_client_key'] == 'newck'


def test_dict_to_identity():
    Obj = {
        'name': "TestGroup",
        'description': "A test group",
        'is_locking': True,
        'client_key':
        'testclientkey',
        'modified': '2012-01-01 01:01:01',
        'created': '2012-01-01 01:01:01',
        "id": 1,
    }
    group = Group(
        id=-1,
        name='',
        description='',
        is_locking=False,
        client_key=''
    ).identity_from_jsonObject(Obj)
    assert isinstance(group, Group)
    assert group.name == 'TestGroup'


def test_json_to_identity():
    jsonStr = '{"description": "A test group", "id": 1, "name": "TestGroup", "created": "2012-01-01 01:01:01", "modified": "2012-01-01 01:01:01", "client_key": "testclientkey", "is_locking": true}'
    group = Group(
        id=-1,
        name='',
        description='',
        is_locking=False,
        client_key=''
    ).identity_from_json(jsonStr)
    assert isinstance(group, Group)
    assert group.name == 'TestGroup'


def test_get_by_id(handler, mocker, group_get_by_id):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_get_by_id)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(id=1)
    assert res.id == 1
    assert res.name == 'BRP:M0536B4E2DDLA7W6'


def test_get_by_name(handler, mocker, group_get_by_id):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_get_by_id)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(name='BRP:M0536B4E2DDLA7W6')
    assert res.id == 1
    assert res.name == 'BRP:M0536B4E2DDLA7W6'


def test_get_badparams(handler, mocker, group_get_by_id):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_get_by_id)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.InvalidArguments):
        handler.get(foo='bar')


def test_get_group_subjects(handler, mocker, group_get_subjects):
    grp = Group(
        id=1,
        name='BRP:M0536B4E2DDLA7W6',
        description='Test Group',
        is_locking=True,
        client_key='testck'
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_get_subjects)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get_subjects(grp)
    assert len(res) == 1
    assert res[0].first_name == 'John'
    assert res[0].last_name == 'Sample'


def test_add_subject_to_group(handler, mocker, group_add_sub_to_group_success):
    grp = Group(
        id=1,
        name='BRP:M0536B4E2DDLA7W6',
        description='Test Group',
        is_locking=True,
        client_key='testck'
    )
    sub = Subject(
        id=2,
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_add_sub_to_group_success)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.add_subjects(grp, [sub])[0]
    assert res['success']


def test_remove_subject_from_group(handler, mocker):
    grp = Group(
        id=1,
        name='BRP:M0536B4E2DDLA7W6',
        description='Test Group',
        is_locking=True,
        client_key='testck'
    )
    sub = Subject(
        id=2,
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.remove_subject(grp, sub)


def test_get_records_from_group(handler, mocker, group_get_group_records):
    grp = Group(
        id=1,
        name='BRP:M0536B4E2DDLA7W6',
        description='Test Group',
        is_locking=True,
        client_key='testck'
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_get_group_records)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get_records(grp)[0]
    assert isinstance(res, ExternalRecord)


def test_add_records_to_group(handler, mocker):
    grp = Group(
        id=1,
        name='BRP:M0536B4E2DDLA7W6',
        description='Test Group',
        is_locking=True,
        client_key='testck'
    )
    record = ExternalRecord(
        id=1,
        record_id='test'
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'[{"id": 1, "success": true}]')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.add_records(grp, [record])[0]
    assert res['success']


def test_remove_records_from_group(handler, mocker):
    grp = Group(
        id=1,
        name='BRP:M0536B4E2DDLA7W6',
        description='Test Group',
        is_locking=True,
        client_key='testck'
    )
    record = ExternalRecord(
        id=1,
        record_id='test'
    )
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.remove_record(grp, record)


def test_delete_group_by_id(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(id=1, client_key='testck')


def test_delete_group_by_name(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(name='BRP:M0536B4E2DDLA7W6', client_key='testck')


def test_delete_group_nock(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.InvalidArguments):
        handler.delete(name='BRP:M0536B4E2DDLA7W6')


def test_create_group(handler, mocker, group_create):
    grp = Group(
        id=3,
        name='Test Group',
        description='a test group',
        is_locking=True,
        client_key='testck'
    )
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_create)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.create(grp)[0]
    assert res['success']


def test_create_update(handler, mocker, group_update):
    grp = Group(
        id=3,
        name='Test Group',
        description='a test group',
        is_locking=True,
        client_key='testck'
    )
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_update)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(grp)[0]
    assert res['success']


def test_create_update_name(handler, mocker, group_update_name):
    grp = Group(
        id=3,
        name='Test Group',
        description='a test group',
        is_locking=True,
        client_key='testclientkey'
    )
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=group_update_name)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(grp)[0]
    assert res['success']
