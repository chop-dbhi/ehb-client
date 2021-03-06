import pytest
import datetime
from ehb_client.requests.request_handler import RequestHandler
from ehb_client.requests.request_handler import client
from ehb_client.requests.subj_fam_relationships_handler import SubjFamRelationship, \
    SubjFamRelationshipRequestHandeler


@pytest.fixture(scope='module')
def handler():
    return SubjFamRelationshipRequestHandeler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


def test_create(handler, mocker, relationship_create_response):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    subjFam = SubjFamRelationship(
        subject_1_id=1,
        subject_2_id=2,
        subject_1_role=4,
        subject_2_role=4,
        protocol_id=1,
        id=1,
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    eHBResponse.read = mocker.MagicMock(return_value=relationship_create_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.create(subjFam)[0]
    assert res['success']
    assert isinstance(res['subjFamRelationship'], SubjFamRelationship)


def test_get_by_subject(handler, mocker, relationship_get_by_subject):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=relationship_get_by_subject)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(subject_id=1)
    assert res[0].subject_1_id == 1
    assert res[0].subject_1_role == "Brother"


def test_get_by_protocol_id(handler, mocker, relationship_get_by_protocol):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=relationship_get_by_protocol)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(protocol_id=1)
    assert res[0].subject_1_id == 1
    assert res[0].subject_1_role == "Brother"


def test_delete_relationship_by_id(handler, mocker):

    eHBResponse = mocker.MagicMock(
        status=204
    )
    eHBResponse.read = mocker.MagicMock(return_value=b'')
    handler.request_handler.DELETE = mocker.MagicMock(return_value=eHBResponse)
    handler.delete(relationship_id=1)
