import pytest
import datetime
from ehb_client.requests.request_handler import RequestHandler
from ehb_client.requests.request_handler import client
from ehb_client.requests.pedigree_relationships_handler import PedigreeRelationship, \
    PedigreeRelationshipRequestHandeler


@pytest.fixture(scope='module')
def handler():
    return PedigreeRelationshipRequestHandeler(
        host='example.com',
        root_path='',
        secure=False,
        api_key='testkey'
    )


# TODO update for relationships.
def test_create(handler, mocker, relationship_create_response):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    pedigree = PedigreeRelationship(
        subject_1=1,
        subject_2=2,
        subject_1_role=4,
        subject_2_role=4,
        protocol_id=1,
        id=1,
        modified=datetime.datetime(2015, 1, 1),
        created=datetime.datetime(2015, 1, 1)
    )
    eHBResponse.read = mocker.MagicMock(return_value=relationship_create_response)
    handler.request_handler.POST = mocker.MagicMock(return_value=eHBResponse)
    res = handler.create(pedigree)[0]
    assert res['success']
    assert isinstance(res['PedigreeRelationship'], PedigreeRelationship)


# TODO update for get relationships for given subject
def test_get_by_subject(handler, mocker, relationship_get_by_subject):
    eHBResponse = mocker.MagicMock(
        status=200
    )
    eHBResponse.read = mocker.MagicMock(return_value=relationship_get_by_subject)
    handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
    res = handler.get(subject_id=1)
    assert isinstance(res, PedigreeRelationship)
    assert res.subject_1 == 1

# # TODO update for get relationships for given protocol
# def test_get_by_id(handler, mocker, subject_get_by_id):
#     eHBResponse = mocker.MagicMock(
#         status=200
#     )
#     eHBResponse.read = mocker.MagicMock(return_value=subject_get_by_id)
#     handler.request_handler.GET = mocker.MagicMock(return_value=eHBResponse)
#     res = handler.get(id=1)
#     assert isinstance(res, Subject)
#     assert res.first_name == 'John'
