import pytest
import json
import datetime
from ehb_client.requests.group_request_handler import Group, \
    GroupRequestHandler

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
    print(res)
    assert False
