import pytest
from ehb_client.requests.external_record_request_handler import ExternalRecordRelationRequestHandler


@pytest.fixture(scope='module')
def handler():
    return ExternalRecordRelationRequestHandler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return ExternalRecordRelationRequestHandler(
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
    eHBResponse.read = mocker.MagicMock(return_value=b'[{"typ": "familial", "id": 1, "desc": "Parent of"}, {"typ": "diagnosis", "id": 2, "desc": "Associated Diagnosis"}]')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    response = handler.get()
    assert isinstance(response, list)
    assert len(response) == 2


def test_get_bad_response(handler, mocker):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'BADJSON')
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    response = handler.get()
    assert isinstance(response, dict)
    assert response['error'] == 'invalid JSON received from eHB'
