import pytest
import json
import datetime
from ehb_client.requests.external_record_request_handler import ExternalRecord, \
    ExternalRecordRequestHandler

from ehb_client.requests import exceptions


@pytest.fixture(scope='module')
def handler():
    return ExternalRecordRequestHandler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return ExternalRecordRequestHandler(
        host='example.com',
        root_path='',
        secure=True,
        api_key='testkey'
    )


def test_handler_initialization(handler):
    assert handler.host == 'example.com'
    assert handler.root_path == '/api/externalrecord/'
    assert not handler.secure
    assert handler.request_handler.api_key == 'testkey'


def test_secure_handler_initialization(secure_handler):
    assert secure_handler.host == 'example.com'
    assert secure_handler.root_path == '/api/externalrecord/'
    assert secure_handler.secure
    assert secure_handler.request_handler.api_key == 'testkey'


def test_identity_from_json():
    json_string = {
        'external_system': 1,
        'subject': 1,
        'modified': '2012-01-01 01:01:01',
        'created': '2012-01-01 01:01:01',
        'id': 1,
        'record_id': 'xyz123',
        'label': 1,
    }
    ExRecObject = ExternalRecord(record_id=-1).identity_from_json(json.dumps(json_string))
    assert isinstance(ExRecObject, ExternalRecord)
    assert ExRecObject.id == 1
    assert ExRecObject.subject_id == 1
    assert ExRecObject.record_id == 'xyz123'
    assert ExRecObject.label_id == 1
    assert isinstance(ExRecObject.modified, datetime.datetime)
    assert isinstance(ExRecObject.created, datetime.datetime)


def test_json_from_identity():
    ExRecObject = ExternalRecord(
        record_id='xyz123',
        external_system_id=1,
        subject_id=1,
        path='testpath',
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
        id=1,
        label_id=1
    )
    json_string = ExRecObject.json_from_identity(ExRecObject)
    assert isinstance(json_string, str)
    ex_rec = json.loads(json_string)
    assert isinstance(ex_rec, dict)
    assert ex_rec['id'] == 1


def test_json_from_identity_no_label():
    ExRecObject = ExternalRecord(
        record_id='xyz123',
        external_system_id=1,
        subject_id=1,
        path='testpath',
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
        id=1,
        label_id=None
    )
    json_string = ExRecObject.json_from_identity(ExRecObject)
    assert isinstance(json_string, str)
    ex_rec = json.loads(json_string)
    assert isinstance(ex_rec, dict)
    assert ex_rec['id'] == 1


def test_get(handler, mocker, external_record_get):
    eHBResponse = mocker.MagicMock(
        status=200

    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_get)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(id=1)
    assert isinstance(record, ExternalRecord)


def test_get_w_subject_id(handler, mocker, external_record_get, external_record_query):
    ''' Attempts to get an ExternalRecord with keyword arguments
    will result in a query to the eHB for that record
    '''
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    records = handler.get(subject_id=1)
    assert isinstance(records, list)
    assert isinstance(records[0], ExternalRecord)


def test_get_w_subject_org_and_subject_org_id(handler, mocker, external_record_query):
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(subject_org=1, subject_org_id="mrn123")[0]
    assert isinstance(record, ExternalRecord)


def test_get_w_subject_org_and_subject_org_id_bad_resp(handler, mocker, external_record_query_error):
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query_error)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.PageNotFound):
        handler.get(subject_org=1, subject_org_id="mrn123")[0]


def test_get_w_external_system_id(handler, mocker, external_record_query):
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(external_system_id=1)[0]
    assert isinstance(record, ExternalRecord)


def test_get_w_external_system_name(handler, mocker, external_record_query):
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(external_system_name="testexternalsystem")[0]
    assert isinstance(record, ExternalRecord)


def test_get_w_external_system_url(handler, mocker, external_record_query):
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(external_system_url="http://example.com")[0]
    assert isinstance(record, ExternalRecord)


def test_get_w_path(handler, mocker, external_record_query):
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(path="testpath")[0]
    assert isinstance(record, ExternalRecord)


def test_get_w_label_id(handler, mocker, external_record_query):
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(subject_id=1, label_id=1)[0]
    assert isinstance(record, ExternalRecord)


def test_get_improper_kwargs(handler, mocker, external_record_get, external_record_query):
    ''' Attempts to get an ExternalRecord with keyword arguments
    will result in a query to the eHB for that record
    '''
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.InvalidArguments):
        handler.get(label_id=1)[0]


def test_get_not_found(handler, mocker, external_record_get, external_record_query):
    ''' Attempts to get an ExternalRecord with keyword arguments
    will result in a query to the eHB for that record
    '''
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=404
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    with pytest.raises(exceptions.PageNotFound):
        handler.get(subject_id=1)[0]


def test_get_links(handler, mocker, external_record_get, external_record_get_links):
    ''' Attempts to get an ExternalRecord with keyword arguments
    will result in a query to the eHB for that record
    '''
    handler.request_handler.POST = mocker.MagicMock()
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_get_links)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    record = handler.get(id=1, links=True)[0]
    assert handler.request_handler.POST.is_called
    assert isinstance(record, dict)
    assert record['primary']
    assert record['type'] == 'familial'
    assert record['description'] == 'Parent of'


def test_query(handler, mocker, external_record_query):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    records = handler.query()[0]
    assert len(records['external_record']) == 2


def test_query_w_subject(handler, mocker, external_record_query):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    records = handler.query({"subject_id": 1})[0]
    assert len(records['external_record']) == 2


def test_query_error(handler, mocker, external_record_query_error):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query_error)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    records = handler.query()[0]
    assert records['path'] == 'not_provided'
    assert records['subject'] == 'not_provided'
    assert not records['success']
    assert {'id': 8} in records['errors']
    assert records['external_system'] == 'not_provided'


def test_delete_record(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(id=1)


def test_delete_record_kwargs(handler, mocker, external_record_query):
    eHBResponseDelete = mocker.MagicMock(
        status=204
    )
    eHBResponseDelete.read = mocker.MagicMock(return_value=b'')
    eHBResponsePost = mocker.MagicMock(
        status=200
    )
    eHBResponsePost.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponseDelete)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponsePost)
    handler.delete(external_system_id=1)


def test_delete_record_kwargs_error(handler, mocker, external_record_query_error):
    eHBResponseDelete = mocker.MagicMock(
        status=204
    )
    eHBResponseDelete.read = mocker.MagicMock(return_value=b'')
    eHBResponsePost = mocker.MagicMock(
        status=200
    )
    eHBResponsePost.read = mocker.MagicMock(return_value=external_record_query_error)
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponseDelete)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponsePost)
    with pytest.raises(exceptions.PageNotFound):
        handler.delete(external_system_id=1)


def test_delete_record_improperkwargs(handler, mocker, external_record_query_error):
    eHBResponseDelete = mocker.MagicMock(
        status=204
    )
    eHBResponseDelete.read = mocker.MagicMock(return_value=b'')
    eHBResponsePost = mocker.MagicMock(
        status=200
    )
    eHBResponsePost.read = mocker.MagicMock(return_value=external_record_query_error)
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponseDelete)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponsePost)
    with pytest.raises(exceptions.InvalidArguments):
        handler.delete(label_id=1)


def test_create_record(handler, mocker, external_record_create):
    ExRecObject = ExternalRecord(
        record_id='xyz123',
        external_system_id=1,
        subject_id=1,
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
        id=1,
        label_id=1
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_create)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    response = handler.create(ExRecObject)
    assert isinstance(response[0]['external_record'], ExternalRecord)


def test_create_record_w_path(handler, mocker, external_record_create_w_path):
    ExRecObject = ExternalRecord(
        record_id='xyz123',
        external_system_id=1,
        subject_id=1,
        path='testpath',
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
        id=1,
        label_id=1
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_create_w_path)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    response = handler.create(ExRecObject)
    response = handler.create(ExRecObject)
    assert isinstance(response[0]['external_record'], ExternalRecord)


def test_link_record(handler, mocker, external_record_link):
    er1 = mocker.MagicMock(
        id=10
    )
    er2 = mocker.MagicMock(
        id=1
    )
    linkType = 1
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_link)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    result = handler.link(er1, er2, linkType)
    assert result['success']


def test_link_record_delete(handler, mocker):
    er1 = mocker.MagicMock(
        id=10
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'{"success": true}')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    response = handler.unlink(er1, 2)
    assert response['success']


def test_update_record(handler, mocker, external_record_update_response):
    ExRecObject = ExternalRecord(
        record_id='xyz123',
        external_system_id=1,
        subject_id=1,
        path='testpath',
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
        id=1,
        label_id=1
    )
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_update_response)
    handler.request_handler.PUT = mocker.MagicMock(return_value=eHBResponse)
    response = handler.update(ExRecObject)
    print(response)
    assert isinstance(response[0]['external_record'], ExternalRecord)
    assert response[0]['success']
    assert not response[0]['errors']
