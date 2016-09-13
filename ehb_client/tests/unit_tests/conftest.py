import pytest


@pytest.fixture(scope='module')
def external_record_get():
    return b'{"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:I5CPQ07I5", "path": "Demo", "external_system": 1, "id": 1, "subject": 1}'


@pytest.fixture(scope='module')
def external_record_get_links():
    return b'[{"external_record": {"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:I5CPQ07I5", "path": "Demo", "external_system": 1, "id": 1, "subject": 1}, "type": "familial", "description": "Parent of", "primary": true, "id": 1}]'


@pytest.fixture(scope='module')
def external_record_query():
    return b'[{"external_record": [{"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:I5CPQ07I5", "path": "Demo", "external_system": 1, "id": 1, "subject": 1}, {"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:XM5VUKTNY", "path": "Demo", "external_system": 1, "id": 2, "subject": 1}], "path_": "not_provided", "external_system_": "not_provided", "subject_": "not_provided"}]'


@pytest.fixture(scope='module')
def external_record_query_error():
    return b'[{"id":1,"success":false,"errors":[{"id":8}]}]'


@pytest.fixture(scope='module')
def external_record_create():
    return b'[{"success": true, "created": "2016-9-12 12:52:27", "modified": "2016-9-12 12:52:27", "label_id": 1, "record_id": "xyz123", "id": "10"}]'


@pytest.fixture(scope='module')
def external_record_create_w_path():
    return b'[{"success": true, "created": "2016-9-12 13:0:1", "modified": "2016-9-12 13:0:1", "label_id": 1, "record_id": "xyz123", "path": "testpath", "id": "11"}]'


@pytest.fixture(scope='module')
def external_record_link():
    return b'{"external_record": "10", "success": true, "created": "2016-9-12 13:49:10", "related_record": 1, "relation_type": 1, "modified": "2016-9-12 13:49:10", "id": "2"}'


@pytest.fixture(scope='module')
def external_record_update_response():
    return b'[{"created": "2015-9-29 13:51:16", "id": "1", "success": true, "modified": "2016-9-12 15:53:48"}]'
