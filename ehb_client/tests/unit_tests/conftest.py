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


@pytest.fixture(scope='module')
def external_system_get():
    return b'{"description": "CHOP\'s REDCap Instance", "created": "2015-09-29 12:03:50.196000", "url": "https://redcap.chop.edu/api/", "modified": "2015-09-29 12:03:50.196000", "id": "1", "name": "REDCap"}'


@pytest.fixture(scope='module')
def external_system_query_url():
    return b'[{"url": "http://example.com/noop/", "externalSystem": {"description": "Placeholder for external IDs", "created": "2016-01-10 15:35:41.311000", "url": "http://example.com/noop/", "modified": "2016-01-10 15:35:41.311000", "id": "3", "name": "External Identifiers"}}]'


@pytest.fixture(scope='module')
def external_system_query_name():
    return b'[{"externalSystem": {"description": "Placeholder for external IDs", "created": "2016-01-10 15:35:41.311000", "url": "http://example.com/noop/", "modified": "2016-01-10 15:35:41.311000", "id": "3", "name": "External Identifiers"}, "name": "External Identifiers"}]'


@pytest.fixture(scope='module')
def external_system_query_not_found_url():
    return b'[{"url": "http://ec", "errors": [{"Query": 9}]}]'


@pytest.fixture(scope='module')
def external_system_query_not_found_name():
    return b'[{"name": "foo", "errors": [{"Query": 9}]}]'


@pytest.fixture(scope='module')
def external_system_get_records():
    return b'[{"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:I5CPQ07I5", "path": "Demo", "external_system": 1, "id": 1, "subject": 1}, {"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:XM5VUKTNY", "path": "Demo", "external_system": 1, "id": 2, "subject": 1}]'


@pytest.fixture(scope='module')
def external_system_get_subjects():
    return b'[{"first_name": "John", "last_name": "Sample", "created": "2015-09-29 12:09:05.202000", "dob": "2000-01-01", "modified": "2015-09-29 12:09:05.202000", "organization_subject_id": "42424242", "organization": 1, "id": 1}]'


@pytest.fixture(scope='module')
def external_system_create():
    return b'[{"name": "Test System", "created": "2016-9-21 20:31:13", "id": "4", "success": true, "modified": "2016-9-21 20:31:13"}]'


@pytest.fixture(scope='module')
def external_system_update():
    return b'[{"created": "2015-9-29 12:3:50", "id": "1", "success": true, "modified": "2016-9-21 21:5:56"}]'


@pytest.fixture(scope='module')
def external_system_update_name():
    return b'[{"created": "2015-9-29 12:3:50", "name": "Updated External System", "success": true, "modified": "2016-9-21 21:5:56"}]'


@pytest.fixture(scope='module')
def external_system_update_url():
    return b'[{"created": "2015-9-29 12:3:50", "url": "http://bar.com/", "success": true, "modified": "2016-9-21 21:5:56"}]'


@pytest.fixture(scope='module')
def group_get_by_id():
    return b'{"ehb_key": "MKDKB9W48SLSFM4A", "description": "A BRP Protocol Group", "created": "2015-09-29 12:01:41.692000", "modified": "2015-09-29 12:01:41.692000", "is_locking": "True", "id": "1", "name": "BRP:M0536B4E2DDLA7W6"}'


@pytest.fixture(scope='module')
def group_get_subjects():
    return b'[{"first_name": "John", "last_name": "Sample", "created": "2015-09-29 12:09:05.202000", "dob": "2000-01-01", "modified": "2015-09-29 12:09:05.202000", "organization_subject_id": "42424242", "organization": 1, "id": 1}]'


@pytest.fixture(scope='module')
def group_add_sub_to_group_success():
    return b'[{"id": 1, "success": true}]'


@pytest.fixture(scope='module')
def group_get_group_records():
    return b'[{"created": "2015-09-29 13:51:16.189000", "modified": "2015-09-29 13:51:16.190000", "label": 1, "record_id": "S891XSB0XD1NKRPF:I5CPQ07I5", "path": "Demo", "external_system": 1, "id": 1, "subject": 1}]'


@pytest.fixture(scope='module')
def group_create():
    return b'[{"ehb_key": "6ZD44324ATZRXT0U", "name": "TestGroup", "success": true, "created": "2016-9-23 13:20:10", "modified": "2016-9-23 13:20:10", "id": "3"}]'


@pytest.fixture(scope='module')
def group_update():
    return b'[{"ehb_key": "6ZD44324ATZRXT0U", "created": "2016-9-23 13:20:10", "id": "3", "success": true, "modified": "2016-9-23 13:36:29"}]'


@pytest.fixture(scope='module')
def group_update_name():
    return b'[{"ehb_key": "6ZD44324ATZRXT0U", "created": "2016-9-23 13:20:10", "name": "Test Group", "success": true, "modified": "2016-9-23 13:36:29"}]'


@pytest.fixture(scope='module')
def org_query_response():
    return b'[{"organization": {"id": "1", "subject_id_label": "Record ID", "name": "Amazing Children\'s Hospital", "modified": "2015-09-29 12:01:11.191000", "created": "2015-09-29 12:01:11.191000"}, "name": "Amazing Children\'s Hospital"}]'


@pytest.fixture(scope='module')
def org_query_bad_response():
    return b'[{"errors": [{"Query": 9}], "name": "foo"}]'


@pytest.fixture(scope='module')
def org_get():
    return b'{"id": "1", "subject_id_label": "Record ID", "name": "Amazing Children\'s Hospital", "modified": "2015-09-29 12:01:11.191000", "created": "2015-09-29 12:01:11.191000"}'


@pytest.fixture(scope='module')
def org_create_response():
    return b'[{"name": "Test Organization", "created": "2016-9-23 15:42:39", "id": "2", "success": true, "modified": "2016-9-23 15:42:39"}]'


@pytest.fixture(scope='module')
def org_update_response():
    return b'[{"created": "2015-9-29 12:1:11", "id": "1", "success": true, "modified": "2016-9-23 15:46:12"}]'


@pytest.fixture(scope='module')
def subject_get_by_id():
    return b'{"first_name": "John", "last_name": "Sample", "created": "2015-09-29 12:09:05.202000", "dob": "2000-01-01", "modified": "2015-09-29 12:09:05.202000", "organization_subject_id": "42424242", "organization": 1, "id": 1}'


@pytest.fixture(scope='module')
def subject_get_org_info():
    return subject_get_by_id()


@pytest.fixture(scope='module')
def subject_create_response():
    return b'[{"success": true, "created": "2016-9-23 16:32:11", "modified": "2016-9-23 16:32:11", "organization_id": 1, "organization_subject_id": "MRN123", "id": "2"}]'


@pytest.fixture(scope='module')
def subject_update_response():
    return b'[{"created": "2016-9-23 16:32:11", "id": "2", "success": true, "modified": "2016-9-23 16:36:24"}]'


@pytest.fixture(scope='module')
def subject_update_response2():
    return b'[{"created": "2016-9-23 16:32:11", "organization_id": "1", "organization_subject_id": "MRN123", "success": true, "modified": "2016-9-23 16:36:24"}]'


@pytest.fixture(scope='module')
def subject_update_badresponse():
    return b'[{"errors": [{"id": 1}], "id": "34", "success": false}]'


@pytest.fixture(scope='module')
def relationship_create_response():
    return b'[{"success": true, "created": "2018-9-21 15:0:22", "subject_1_role": 1, "protocol_id": "1", "modified": "2018-9-21 15:0:22", "subject_1": 2, "subject_2_role": 4, "id": "1"}]'


@pytest.fixture(scope='module')
def relationship_get_by_subject():
    json_string = """{"related_subject_id": 2,
                "related_subject_org": "AMAZING CHILDREN'S HOSPITAL",
                "related_subject_org_id": "JULYTEST",
                "role": "Brother",
                "subject_id": 1,
                "subject_org": "AMAZING CHILDREN\'S HOSPITAL",
                "subject_org_id": "MRN123"},
                {"related_subject_id": 1,
                "related_subject_org": "AMAZING CHILDREN\'S HOSPITAL",
                "related_subject_org_id": "MRN123",
                "role": "Sister",
                "subject_id": 2,
                "subject_org": "AMAZING CHILDREN\'S HOSPITAL",
                "subject_org_id": "JULYTEST"} """
    return json_string.encode()
