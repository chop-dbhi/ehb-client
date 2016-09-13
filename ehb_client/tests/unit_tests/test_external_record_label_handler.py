import pytest
from ehb_client.requests.external_record_request_handler import ExternalRecordLabelRequestHandler


@pytest.fixture(scope='module')
def handler():
    return ExternalRecordLabelRequestHandler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return ExternalRecordLabelRequestHandler(
        host='example.com',
        root_path='',
        secure=True,
        api_key='testkey'
    )


def test_handler_initialization(handler):
    assert handler.host == 'example.com'
    assert handler.root_path == ''
    assert not handler.secure
    assert handler.request_handler.api_key == 'testkey'


def test_secure_handler_initialization(secure_handler):
    assert secure_handler.host == 'example.com'
    assert secure_handler.root_path == ''
    assert secure_handler.secure
    assert secure_handler.request_handler.api_key == 'testkey'


def test_create(handler):
    assert not handler.create()


def test_delete(handler):
    assert not handler.delete()


def test_update(handler):
    assert not handler.update()


def test_get(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'{"id": 1, "label": ""}')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    response = handler.get(id=1)
    assert isinstance(response, dict)
    assert response['id'] == 1
    assert response['label'] == ''


def test_get_bad_response(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'BADJSON')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    response = handler.get(id=1)
    assert isinstance(response, dict)
    assert response['error'] == 'invalid JSON received from eHB'


def test_query(handler, mocker):
    ''' Note: the query function on this handler is very naive. It simply
    returns all labels'''
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'[{"id": 1, "label": ""}, {"id": 2, "label": "SSN"}, {"id": 3, "label": "Initial Diagnosis"}]')
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    response = handler.query()
    assert isinstance(response, list)
    assert len(response) == 3


def test_query_bad_response(handler, mocker):
    ''' Note: the query function on this handler is very naive. It simply
    returns all labels'''
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'BADJSON')
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    response = handler.query()
    assert isinstance(response, dict)
    assert response['error'] == 'invalid JSON received from eHB'
