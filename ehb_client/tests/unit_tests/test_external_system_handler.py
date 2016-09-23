import pytest
import json
import datetime
from ehb_client.requests.external_system_request_handler import ExternalSystem, \
    ExternalSystemRequestHandler
from ehb_client.requests.external_record_request_handler import ExternalRecord
from ehb_client.requests.subject_request_handler import Subject

from ehb_client.requests import exceptions


@pytest.fixture(scope='module')
def handler():
    return ExternalSystemRequestHandler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return ExternalSystemRequestHandler(
        host='example.com',
        root_path='',
        secure=True,
        api_key='testkey'
    )


def test_handler_initialization(handler):
    assert handler.host == 'example.com'
    assert handler.root_path == '/api/externalsystem/'
    assert not handler.secure
    assert handler.request_handler.api_key == 'testkey'


def test_secure_handler_initialization(secure_handler):
    assert secure_handler.host == 'example.com'
    assert secure_handler.root_path == '/api/externalsystem/'
    assert secure_handler.secure
    assert secure_handler.request_handler.api_key == 'testkey'


def test_identity_from_json():
    jsonObj = {
        'id': 1,
        'name': 'Test System',
        'description': 'Test External System for unit tests',
        'url': 'http://example.com/api/',
        'modified': '2012-01-01 01:01:01',
        'created': '2012-01-01 01:01:01',
    }
    ExSysObject = ExternalSystem(
        id=-1,
        name='foo',
        description='bar',
        url='http://foo.com'
    ).identity_from_json(json.dumps(jsonObj))
    assert isinstance(ExSysObject, ExternalSystem)
    assert ExSysObject.id == 1
    assert ExSysObject.name == 'Test System'
    assert ExSysObject.description == 'Test External System for unit tests'
    assert isinstance(ExSysObject.modified, datetime.datetime)
    assert isinstance(ExSysObject.created, datetime.datetime)


def test_json_from_identity():
    ExSysObject = ExternalSystem(
        id=1,
        name='Test System',
        description='Test External System for unit tests',
        url='http://example.com/api/',
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
    )
    json_string = ExSysObject.json_from_identity(ExSysObject)
    assert isinstance(json_string, str)
    ex_rec = json.loads(json_string)
    assert isinstance(ex_rec, dict)
    assert ex_rec['id'] == 1


def test_correct_exsys_url():
    ExSysObject = ExternalSystem(
        id=1,
        name='Test System',
        description='Test External System for unit tests',
        url='http://example.com/api',
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
    )
    assert ExSysObject.url == 'http://example.com/api/'


def test_query_by_name(handler, mocker, external_system_query_name):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_name)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.query({'name': 'External Identifiers'})[0]
    assert isinstance(res['external_system'], ExternalSystem)
    assert res['success']


def test_query_by_url(handler, mocker, external_system_query_url):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_url)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.query({'url': 'http://example.com/api'})[0]
    assert isinstance(res['external_system'], ExternalSystem)
    assert res['success']


def test_query_none_found_url(handler, mocker, external_system_query_not_found_url):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_not_found_url)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.query({'url': 'http://error.com/api'})[0]
    assert not res['success']
    assert res['errors'][0]['Query'] == 9


def test_query_none_found_name(handler, mocker, external_system_query_not_found_name):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_not_found_name)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.query({'name': 'foo'})[0]
    assert not res['success']
    assert res['errors'][0]['Query'] == 9


def test_get_external_system_records_by_exsys_id(handler, mocker, external_system_get_records):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_records)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.external_records(1)
    assert len(res) == 2
    assert isinstance(res[0], ExternalRecord)


def test_get_external_system_records_by_exsys_and_org_id(handler, mocker, external_system_get_records):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_records)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.external_records(1, organization_id=1)
    assert len(res) == 2
    assert isinstance(res[0], ExternalRecord)


def test_get_external_system_records_by_exsys_and_bad_path(handler, mocker, external_system_get_records):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_records)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.PageNotFound):
        handler.external_records(1, path='test_path')


def test_get_external_system_records_by_exsys_and_path(handler, mocker, external_system_get_records):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_records)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.external_records(1, path='Demo')
    assert len(res) == 2
    assert isinstance(res[0], ExternalRecord)


def test_get_external_system_records_by_exsys_path_and_subject_id(handler, mocker, external_system_get_records):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_records)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.external_records(1, path='Demo', subject_id=1)
    assert len(res) == 2
    assert isinstance(res[0], ExternalRecord)


def test_get_external_system_records_by_exsys_subject_id(handler, mocker, external_system_get_records):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_records)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.external_records(1, subject_id=1)
    assert len(res) == 2
    assert isinstance(res[0], ExternalRecord)


def test_get_external_system_subjects_by_exsys(handler, mocker, external_system_get_subjects):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_subjects)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.subjects(1)
    assert len(res) == 1
    assert isinstance(res[0], Subject)


def test_get_external_system_subjects_none_found(handler, mocker, external_system_get_subjects):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'[]')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.PageNotFound):
        handler.subjects(1)


def test_get_external_system_subjects_none_found_with_path(handler, mocker, external_system_get_subjects):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'[]')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    handler.external_records = mocker.MagicMock(return_value=[])
    with pytest.raises(exceptions.PageNotFound):
        handler.subjects(1, path='Demo')


def test_get_external_system_subjects_by_orgid(handler, mocker, external_system_get_subjects):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_subjects)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.subjects(1, organization_id=1)
    assert len(res) == 1
    assert isinstance(res[0], Subject)


def test_get_external_system_subjects_by_path(handler, mocker, external_system_get_subjects):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get_subjects)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    handler.external_records = mocker.MagicMock(return_value=[
        ExternalRecord(
            record_id='xyz123',
            external_system_id=1,
            subject_id=1,
            path='testpath',
            modified=datetime.datetime(2014, 1, 1),
            created=datetime.datetime(2014, 1, 1),
            id=1,
            label_id=None
        )]
    )
    res = handler.subjects(1, path='Demo')
    assert len(res) == 1
    assert isinstance(res[0], Subject)


def test_get_external_system_by_id(handler, mocker, external_system_get):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_get)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(id=1)
    assert isinstance(res, ExternalSystem)
    assert res.id == 1


def test_get_external_system_by_name(handler, mocker, external_system_query_name):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_name)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(name='External Identifiers')
    assert isinstance(res, ExternalSystem)
    assert res.id == 3


def test_get_external_system_by_url(handler, mocker, external_system_query_url):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_url)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(url='http://example.com/noop/')
    assert isinstance(res, ExternalSystem)
    assert res.id == 3


def test_get_external_system_by_url_not_found(handler, mocker, external_system_query_not_found_url):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_not_found_url)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.PageNotFound):
        handler.get(url='http://foo.com/noop/')


def test_get_external_system_by_name_not_found(handler, mocker, external_system_query_not_found_name):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_not_found_name)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.PageNotFound):
        handler.get(name='Non Existent')


def test_get_external_system_by_bad_params(handler, mocker, external_system_query_not_found_name):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_query_not_found_name)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.InvalidArguments):
        handler.get(foo='bar')


def test_delete_by_id(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(id=1)


def test_delete_by_name(handler, mocker, external_system_query_name):
    eHBResponseQuery = mocker.MagicMock(
        status=200
    )
    eHBResponseQuery.read = mocker.MagicMock(return_value=external_system_query_name)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponseQuery)
    eHBResponseDelete = mocker.MagicMock(
        status=204
    )
    eHBResponseDelete.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponseDelete)
    handler.delete(name='External Identifiers')


def test_delete_by_url(handler, mocker, external_system_query_url):
    eHBResponseQuery = mocker.MagicMock(
        status=200
    )
    eHBResponseQuery.read = mocker.MagicMock(return_value=external_system_query_url)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponseQuery)
    eHBResponseDelete = mocker.MagicMock(
        status=204
    )
    eHBResponseDelete.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponseDelete)
    handler.delete(url='http://example.com/noop/')


def test_delete_by_url_badurl(handler, mocker, external_system_query_not_found_url):
    eHBResponseQuery = mocker.MagicMock(
        status=200
    )
    eHBResponseQuery.read = mocker.MagicMock(return_value=external_system_query_not_found_url)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponseQuery)
    eHBResponseDelete = mocker.MagicMock(
        status=204
    )
    eHBResponseDelete.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponseDelete)
    with pytest.raises(exceptions.PageNotFound):
        handler.delete(url='http://foo.com/noop/')


def test_delete_by_url_badname(handler, mocker, external_system_query_not_found_name):
    eHBResponseQuery = mocker.MagicMock(
        status=200
    )
    eHBResponseQuery.read = mocker.MagicMock(return_value=external_system_query_not_found_name)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponseQuery)
    eHBResponseDelete = mocker.MagicMock(
        status=204
    )
    eHBResponseDelete.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponseDelete)
    with pytest.raises(exceptions.PageNotFound):
        handler.delete(name='Non Existent')


def test_delete_bad_params(handler):
    with pytest.raises(exceptions.InvalidArguments):
        handler.delete(foo='bar')


def test_create(handler, mocker, external_system_create):
    ExSys = ExternalSystem(
        id=4,
        name='foo',
        description='bar',
        url='http://foo.com'
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_create)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.create(ExSys)[0]
    assert res['success']


def test_update(handler, mocker, external_system_update):
    ExSys = ExternalSystem(
        id=1,
        name='Updated External System',
        description='foo',
        url='http://bar.com'
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_update)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(ExSys)[0]
    assert res['success']


def test_update_name(handler, mocker, external_system_update_name):
    ExSys = ExternalSystem(
        id=1,
        name='Updated External System',
        description='foo',
        url='http://bar.com'
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_update_name)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(ExSys)[0]
    assert res['success']


def test_update_url(handler, mocker, external_system_update_url):
    ExSys = ExternalSystem(
        id=1,
        name='Updated External System',
        description='foo',
        url='http://bar.com'
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_system_update_url)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    res = handler.update(ExSys)[0]
    assert res['success']
