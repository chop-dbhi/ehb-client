import json
import datetime
from ehb_client.requests.external_record_request_handler import ExternalRecord


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
        id=1
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


def test_query(handler, mocker, external_record_query):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    records = handler.query()[0]
    assert len(records['external_record']) == 2


def test_query_w_params(handler, mocker, external_record_query):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=external_record_query)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    records = handler.query({"subject_id": 1})[0]
    assert len(records['external_record']) == 2
