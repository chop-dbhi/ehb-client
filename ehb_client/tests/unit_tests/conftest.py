import pytest
from ehb_client.requests.external_record_request_handler import \
    ExternalRecordRequestHandler


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


@pytest.fixture(scope='module')
def external_record_get():
    return b'{"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:I5CPQ07I5", "path": "Demo", "external_system": 1, "id": 1, "subject": 1}'


@pytest.fixture(scope='module')
def external_record_query(scope='module'):
    return b'[{"external_record": [{"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:I5CPQ07I5", "path": "Demo", "external_system": 1, "id": 1, "subject": 1}, {"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:XM5VUKTNY", "path": "Demo", "external_system": 1, "id": 2, "subject": 1}], "path_": "not_provided", "external_system_": "not_provided", "subject_": "not_provided"}]'


@pytest.fixture(scope='module')
def external_record_query_error(scope='module'):
    return b'[{"id":1,"success":false,"errors":[{"id":8}]}]'
