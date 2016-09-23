import pytest
import json
import datetime
from ehb_client.requests.subject_request_handler import Subject, \
    SubjectRequestHandler

from ehb_client.requests import exceptions


@pytest.fixture(scope='module')
def handler():
    return SubjectRequestHandler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return SubjectRequestHandler(
        host='example.com',
        root_path='',
        secure=True,
        api_key='testkey'
    )


def test_handler_initialization(handler):
    assert handler.host == 'example.com'
    assert handler.root_path == '/api/subject/'
    assert not handler.secure
    assert handler.request_handler.api_key == 'testkey'


def test_secure_handler_initialization(secure_handler):
    assert secure_handler.host == 'example.com'
    assert secure_handler.root_path == '/api/subject/'
    assert secure_handler.secure
    assert secure_handler.request_handler.api_key == 'testkey'


def test_identity_to_json():
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
    jsonStr = sub.json_from_identity(sub)
    assert isinstance(jsonStr, str)


def test_identity_from_json():
    jsonStr = '{"first_name": "Jane", "organization_subject_id": "MRN123", "dob": "1990-1-1", "last_name": "Sample", "created": "2015-01-01 00:00:00.000000", "organization": 1, "modified": "2015-01-01 00:00:00.000000", "group_name": "", "id": 2}'
    sub = Subject().identity_from_json(jsonStr)
    assert isinstance(sub, Subject)
    assert sub.first_name == 'Jane'


def test_get_by_id(handler, mocker, subject_get_by_id):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=subject_get_by_id)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(id=1)
    assert isinstance(res, Subject)
    assert res.first_name == 'John'


def test_get_by_org_and_org_sub_id(handler, mocker, subject_get_org_info):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=subject_get_org_info)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(organization_id=1, organization_subject_id='42424242')
    assert isinstance(res, Subject)
    assert res.first_name == 'John'


def test_get_badparams(handler, mocker, subject_get_org_info):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=subject_get_org_info)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.InvalidArguments):
        handler.get(foo='bar')


def test_delete_by_id(handler, mocker, subject_get_by_id):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(id=1)


def test_create(handler, mocker, subject_create_response):
    eHBResponse = mocker.MagicMock(
        status=200
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
    eHBResponse.read = mocker.MagicMock(return_value=subject_create_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.create(sub)[0]
    assert res['success']
    assert isinstance(res['subject'], Subject)


def test_update_response(handler, mocker, subject_update_response):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    sub_old = Subject(
        id=2,
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    sub_new = Subject(
        id=2,
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1),
    )
    sub_new.old_subject = sub_old
    eHBResponse.read = mocker.MagicMock(return_value=subject_update_response)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(sub_new)[0]
    assert res['success']


def test_update_with_no_id(handler, mocker, subject_update_response2):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    sub_old = Subject(
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    sub_new = Subject(
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1),
    )
    sub_new.old_subject = sub_old
    eHBResponse.read = mocker.MagicMock(return_value=subject_update_response2)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(sub_new)[0]
    assert res['success']

def test_update_bad_response(handler, mocker, subject_update_badresponse):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    sub_old = Subject(
        id=2,
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    sub_new = Subject(
        id=2,
        first_name='Jane',
        last_name='Sample',
        organization_id=1,
        organization_subject_id='MRN123',
        dob=datetime.datetime(1990, 1, 1),
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1),
    )
    sub_new.old_subject = sub_old
    eHBResponse.read = mocker.MagicMock(return_value=subject_update_badresponse)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(sub_new)[0]
    assert not res['success']
