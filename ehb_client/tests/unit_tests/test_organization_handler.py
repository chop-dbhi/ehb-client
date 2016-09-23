import pytest
import json
import datetime
from ehb_client.requests.organization_request_handler import Organization, \
    OrganizationRequestHandler

from ehb_client.requests import exceptions


@pytest.fixture(scope='module')
def handler():
    return OrganizationRequestHandler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return OrganizationRequestHandler(
        host='example.com',
        root_path='',
        secure=True,
        api_key='testkey'
    )


def test_handler_initialization(handler):
    assert handler.host == 'example.com'
    assert handler.root_path == '/api/organization/'
    assert not handler.secure
    assert handler.request_handler.api_key == 'testkey'


def test_secure_handler_initialization(secure_handler):
    assert secure_handler.host == 'example.com'
    assert secure_handler.root_path == '/api/organization/'
    assert secure_handler.secure
    assert secure_handler.request_handler.api_key == 'testkey'


def test_identity_to_json():
    org = Organization(
        id=1,
        name='Test Organization',
        subject_id_label='Subject',
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    jsonStr = org.json_from_identity(org)
    assert isinstance(jsonStr, str)
    obj = json.loads(jsonStr)
    assert obj['name'] == org.name


def test_identity_from_json():
    jsonStr = {
        "id": 1,
        "name": "Test Organization",
        "subject_id_label": "Subject",
        'modified': '2012-01-01 01:01:01',
        'created': '2012-01-01 01:01:01',
    }
    _org = Organization(
        id=1,
        name='Test Organization',
        subject_id_label='Subject',
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    org = _org.identity_from_json(json.dumps(jsonStr))
    assert org.name == _org.name


def test_query_by_name(handler, mocker, org_query_response):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=org_query_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.query('Amazing Children\'s Hospital')[0]
    assert res['success']
    assert isinstance(res['organization'], Organization)
    assert res['organization'].id == 1


def test_query_by_name_bad_response(handler, mocker, org_query_bad_response):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=org_query_bad_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.query('Amazing Children\'s Hospital')[0]
    assert len(res['errors']) == 1
    assert not res['success']


def test_delete_by_name(handler, mocker, org_query_response):
    eHBResponseQuery = mocker.MagicMock(
        status=200
    )
    eHBResponseQuery.read = mocker.MagicMock(return_value=org_query_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponseQuery)
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(name='Amazing Children\'s Hospital')


def test_delete_by_id(handler, mocker, org_query_response):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(id=1)


def test_delete_by_name_not_found(handler, mocker, org_query_bad_response):
    eHBResponseQuery = mocker.MagicMock(
        status=200
    )
    eHBResponseQuery.read = mocker.MagicMock(return_value=org_query_bad_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponseQuery)
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.PageNotFound):
        handler.delete(name='Amazing Children\'s Hospital')


def test_delete_bad_params(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.InvalidArguments):
        handler.delete(foo=1)


def test_get_by_id(handler, mocker, org_get):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=org_get)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(id=1)
    assert isinstance(res, Organization)
    assert res.id == 1


def test_get_by_name(handler, mocker, org_query_response):
    eHBResponseQuery = mocker.MagicMock(
        status=200
    )
    eHBResponseQuery.read = mocker.MagicMock(return_value=org_query_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponseQuery)
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(name='Amazing Children\'s Hospital')
    assert isinstance(res, Organization)
    assert res.id == 1


def test_create(handler, mocker, org_create_response):
    org = Organization(
        id=1,
        name='Test Organization',
        subject_id_label='Subject',
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=org_create_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.create(org)[0]
    assert res['success']


def test_update(handler, mocker, org_update_response):
    org = Organization(
        id=1,
        name='Test Organization',
        subject_id_label='Research Subject',
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=org_update_response)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(org)[0]
    assert res['success']
