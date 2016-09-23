import pytest
from ehb_client.requests.request_handler import RequestHandler
from ehb_client.requests.request_handler import client
from ehb_client.requests import exceptions


@pytest.fixture(scope='module')
def handler():
    return RequestHandler(
        host='example.com',
        secure=False,
        api_key='testkey'
    )


@pytest.fixture(scope='module')
def secure_handler():
    return RequestHandler(
        host='example.com',
        secure=True,
        api_key='testkey'
    )


def test_handler_initialization(handler):
    assert handler.host == 'example.com'
    assert not handler.secure
    assert handler.api_key == 'testkey'


def test_secure_handler_initialization(secure_handler):
    assert secure_handler.host == 'example.com'
    assert secure_handler.secure
    assert secure_handler.api_key == 'testkey'


def test_append_key(handler):
    headers = {'Content-Type': 'application/json'}
    handler.append_key(headers)
    assert headers['Api-Token'] == 'testkey'


def test_send_request(handler, mocker):
    client.HTTPConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    handler.sendRequest('GET', path='/test/', headers={}, body='')


def test_secure_send_request(secure_handler, mocker):
    client.HTTPSConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    secure_handler.sendRequest('GET', path='/test/', headers={}, body='')


def test_post(secure_handler, mocker):
    client.HTTPSConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    secure_handler.POST(path='/test/', headers={}, body='')


def test_get(secure_handler, mocker):
    client.HTTPSConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    secure_handler.GET(path='/test/', headers={})


def test_put(secure_handler, mocker):
    client.HTTPSConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    secure_handler.PUT(path='/test/', headers={}, body='')


def test_delete(secure_handler, mocker):
    client.HTTPSConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    secure_handler.DELETE(path='/test/', headers={})


def test_head(secure_handler, mocker):
    client.HTTPSConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    secure_handler.HEAD(path='/test/', headers={})


def test_options(secure_handler, mocker):
    client.HTTPSConnection = mocker.MagicMock()
    client.getresponse = mocker.MagicMock()
    secure_handler.OPTIONS(path='/test/', headers={}, body='')
