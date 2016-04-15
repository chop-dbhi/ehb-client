# -*- coding: utf-8 -*-
import datetime
import os
import json
from unittest import TestCase


from ehb_client.requests.subject_request_handler import SubjectRequestHandler, \
    Subject
from ehb_client.requests.external_system_request_handler import ExternalSystem, \
    ExternalSystemRequestHandler
from ehb_client.requests.external_record_request_handler import ExternalRecordRequestHandler, \
    ExternalRecord
from ehb_client.requests.organization_request_handler import Organization, \
    OrganizationRequestHandler
from ehb_client.requests.group_request_handler import Group, \
    GroupRequestHandler
from ehb_client.requests.exceptions import PageNotFound, ErrorConstants, \
    RequestedRangeNotSatisfiable, NotAuthorized


class RequestResources(object):

    host = os.environ.get('EHB_HOST', 'localhost:8000')
    isSecure = False
    root_path = ''
    api_key = os.environ.get('EHB_KEY', '680b8740f60ec65af0163ee7c7959bde')


class ehbTestClass(TestCase):
    '''
    The ehbTestClass is a base class for all ehb-client tests. Its main purpose
    is to create test objects for our different request handlers to manipulate,
    and to tear down those objects when the tests are finished.

    In the rare case that the setUp of a test class fails you may be left with
    artifacts in the eHB. Make sure to delete any "test" organizations left over
    and try running the tests again.
    '''
    def setUp(self):
        # Initialize Request Handlers
        self.er_rh = ExternalRecordRequestHandler(
            RequestResources.host,
            RequestResources.root_path,
            RequestResources.isSecure,
            RequestResources.api_key)
        self.es_rh = ExternalSystemRequestHandler(
            RequestResources.host,
            RequestResources.root_path,
            RequestResources.isSecure,
            RequestResources.api_key)
        self.s_rh = SubjectRequestHandler(
            RequestResources.host,
            RequestResources.root_path,
            RequestResources.isSecure,
            RequestResources.api_key)
        self.g_rh = GroupRequestHandler(
            RequestResources.host,
            RequestResources.root_path,
            RequestResources.isSecure,
            RequestResources.api_key)
        self.o_rh = OrganizationRequestHandler(
            RequestResources.host,
            RequestResources.root_path,
            RequestResources.isSecure,
            RequestResources.api_key)

        self.es_name1 = "testESNameABCD"
        self.es_name2 = "testESName1234"
        self.org_subj_id_1 = "testmrn0001"
        self.org_subj_id_2 = "testmrn0002"
        self.org_subj_id_3 = "testmrn002"
        self.recid1 = "testrecid0001"
        self.recid2 = "testrecid0002"
        self.recid3 = "testrecid0003"
        self.recid4 = "testrecid0004"
        self.path1 = "testpath1"
        self.path2 = "testpath2"
        self.path3 = 'testpath3'
        self.org_name_1 = "testOrg001"
        self.org_name_2 = "testOrg002"
        self.subj_id_label_1 = 'org_1_id'
        try:
            # Create the Organizations
            self.o1 = Organization(name=self.org_name_1,
                                   subject_id_label=self.subj_id_label_1)
            self.o2 = Organization(name=self.org_name_2,
                                   subject_id_label=self.subj_id_label_1)
            r = self.o_rh.create(self.o1, self.o2)

            # Create Subjects
            dob = datetime.date.today()
            self.s1 = Subject(first_name='FIRST_ONE', last_name="LAST_ONE",
                              organization_id=self.o1.id,
                              organization_subject_id=self.org_subj_id_1, dob=dob)
            self.s2 = Subject(first_name='FIRST_TWO', last_name="LAST_TWO",
                              organization_id=self.o1.id,
                              organization_subject_id=self.org_subj_id_2, dob=dob)
            self.s3 = Subject(first_name='FIRST_THREE', last_name="LAST_THREE",
                              organization_id=self.o2.id,
                              organization_subject_id=self.org_subj_id_3, dob=dob)
            r = self.s_rh.create(self.s1, self.s2, self.s3)

            # Create External Systems
            self.es1 = ExternalSystem(name=self.es_name1, url="http://test.com/",
                                      description='A test system')
            self.es2 = ExternalSystem(name=self.es_name2, url="http://testTwo.com/",
                                      description='Another test system')
            r = self.es_rh.create(self.es1, self.es2)

            # Create External record
            self.er1 = ExternalRecord(record_id=self.recid1, subject_id=self.s1.id,
                                      external_system_id=self.es1.id, path=self.path1,
                                      label_id=1)
            self.er2 = ExternalRecord(record_id=self.recid2, subject_id=self.s1.id,
                                      external_system_id=self.es1.id, path=self.path2,
                                      label_id=1)
            r = self.er_rh.create(self.er1, self.er2)
            self.er1 = r[0]['external_record']
            self.er2 = r[1]['external_record']
            # # Create External record link
            r = self.er_rh.link(self.er1, self.er2, 1)
            # Create test groups
            # Subject Group
            self.g1 = Group(name='testgroup1', is_locking=False,
                            client_key='ck', description='A test group')
            # ExternalRecord Group
            self.g2 = Group(name='exrecgroup', is_locking=False,
                            client_key='ck', description='An external record group')
            r = self.g_rh.create(self.g1, self.g2)

            # Add subject to test group
            r = self.g_rh.add_subjects(self.g1, [self.s1])

            # Add external record to test group
            r = self.g_rh.add_records(self.g2, [self.er1])
        except:
            pass

    def tearDown(self):
        try:
            self.es_rh.delete(name=self.es_name1)
        except PageNotFound:
            pass
        try:
            self.es_rh.delete(name=self.es_name2)
        except PageNotFound:
            pass
        try:
            self.es_rh.delete(name='testESNameCreate')
        except PageNotFound:
            pass
        try:
            o1 = self.o_rh.get(name=self.org_name_1)
            self.s_rh.delete(organization_id=o1.id,
                             organization_subject_id=self.org_subj_id_1)
            self.s_rh.delete(organization_id=o1.id,
                             organization_subject_id=self.org_subj_id_2)
        except PageNotFound:
            pass

        try:
            o2 = self.o_rh.get(name=self.org_name_2)
            self.s_rh.delete(organization_id=o2.id,
                             organization_subject_id=self.org_subj_id_3)
        except PageNotFound:
            pass

        try:
            self.er_rh.delete(external_system_name=self.es_name1)
        except PageNotFound:
            pass
        try:
            self.er_rh.delete(external_system_name=self.es_name2)
        except PageNotFound:
            pass

        try:
            self.o_rh.delete(name=self.org_name_1)
        except PageNotFound:
            pass
        try:
            self.o_rh.delete(name=self.org_name_2)
        except PageNotFound:
            pass
        try:
            self.o_rh.delete(name='testorg1')
        except PageNotFound:
            pass
        try:
            self.o_rh.delete(name='testorg2')
        except PageNotFound:
            pass
        try:
            self.o_rh.delete(name='testorg99')
        except PageNotFound:
            pass
        try:
            self.er_rh.create(self.er1)
        except PageNotFound:
            pass

        try:
            self.g_rh.delete(name='testgroup1', client_key='ck')
        except PageNotFound:
            pass
        try:
            self.g_rh.delete(name='exrecgroup', client_key='ck')
        except PageNotFound:
            pass
        try:
            self.g_rh.delete(name='testgroup2', client_key='ck')
        except PageNotFound:
            pass
        try:
            self.g_rh.delete(name='testgroup3', client_key='ck')
        except PageNotFound:
            pass
        try:
            self.g_rh.delete(name='testgroup1xyz', client_key='ck')
        except PageNotFound:
            pass

    def createAndCheck(self, rh, *records):
        r = rh.create(*records)
        b = True

        for i in range(r.__len__()):
            b = b and r[i].get('success')

        self.assertTrue(b, 'External record create failed')


class TestExternalRecordHandler(ehbTestClass):

    def testExternalRecordUpdate(self):
        '''
        Try to update an existing ExternalRecord by updating it's record_id.
        '''
        self.er1.record_id = self.recid3
        r = self.er_rh.update(self.er1)[0]
        self.assertTrue(r.get('success'), 'Single External Record update failed')

    def testExternalRecordDupeCreate(self):
        '''
        Try to create another ExternalRecord with the same record id in the
        same external system with the same path, expect this to return failure
        in status
        '''
        er2 = ExternalRecord(record_id=self.er1.record_id,
                             subject_id=self.er1.subject_id,
                             external_system_id=self.er1.external_system_id,
                             path=self.er1.path)
        r = self.er_rh.create(er2)[0]
        errors = r.get('errors')
        self.assertTrue(len(errors) == 1, 'There should be only one error')
        self.assertTrue(errors[0], ErrorConstants.ERROR_RECORD_ID_ALREADY_IN_EXTERNAL_SYSTEM)
        self.assertFalse(
            r.get('success'),
            'Should not be able to create an ExternalRecord with same record_id, system, and path')

    def testExternalRecordDiffSubjects(self):
        '''
        Try to create another ExternalRecord with the same record id in the
        same external system with the same path but different subjects,
        expect this to return failure in status
        '''
        er = ExternalRecord(record_id=self.er1.record_id, subject_id=self.s2.id,
                            external_system_id=self.er1.external_system_id,
                            path=self.er1.path)
        r = self.er_rh.create(er)[0]
        errors = r.get('errors')
        self.assertTrue(len(errors) == 1, 'Exactly one error expected')
        self.assertTrue(errors[0] == ErrorConstants.ERROR_RECORD_ID_ALREADY_IN_EXTERNAL_SYSTEM)
        self.assertFalse(
            r.get('success'),
            'Should not be able to create an ExternalRecord with same record_id, system, and path')

    def testExternalRecordDelete(self):
        '''
        Try to delete an existing ExternalRecord

        If successful the request handler will not return anything so we check
        for that None value with assertFalse
        '''
        r = self.er_rh.delete(id=self.er1.id)
        self.assertFalse(r, "Should be able to delete an ExternalRecord")

    def testExternalRecordFailedDelete(self):
        '''
        Try to delete an ExternalRecord that does not exists. Expect an
        exception of type PageNotFound
        '''
        try:
            self.assertRaises(self.er_rh.delete(id='bad_id'), PageNotFound)
        except PageNotFound:
            pass

    def testExternalRecordFailedDelete2(self):
        '''
        Try to delete an ExternalRecord that does not exists. Expect an
        exception of type PageNotFound
        '''
        try:
            self.assertRaises(self.er_rh.delete(
                external_system_id='bad_system',
                subject_id=-1
            ), PageNotFound)
        except PageNotFound:
            pass

    def testExternalRecordCreateMulti(self):
        '''
        Try creating multiple ExternalRecords at one time. Expect success.
        '''
        er3 = ExternalRecord(record_id=self.recid3, subject_id=self.s3.id,
                             external_system_id=self.es1.id, path=self.path1)
        er4 = ExternalRecord(record_id=self.recid4, subject_id=self.s1.id,
                             external_system_id=self.es2.id, path=self.path2)
        er5 = ExternalRecord(record_id=self.recid4, subject_id=self.s1.id,
                             external_system_id=self.es2.id, path=self.path1)
        er6 = ExternalRecord(record_id=self.recid1, subject_id=self.s3.id,
                             external_system_id=self.es2.id, path=self.path3)
        self.createAndCheck(self.er_rh, er3, er4, er5, er6)

    def testExternalRecordGetByExternalSystemID(self):
        '''
        Try getting ExternalRecords by ExternalSystem ID
        '''
        r = self.er_rh.get(external_system_id=self.es1.id)
        self.assertTrue(len(r) == 2)

    def testExternalRecordGetByExternalSystemURL(self):
        '''
        Try getting ExternalRecords by ExternalSystem URL
        '''
        r = self.er_rh.get(external_system_url=self.es1.url)
        self.assertTrue(len(r) == 2)

    def testExternalRecordGetByExternalSystemName(self):
        '''
        Try getting ExternalRecords by ExternalSystem Name
        '''
        r = self.er_rh.get(external_system_name=self.es1.name)
        self.assertTrue(len(r) == 2)

    def testExternalRecordGetBySubjectID(self):
        '''
        Try getting ExternalRecords by Subject ID
        '''
        r = self.er_rh.get(subject_id=self.s1.id)
        self.assertTrue(len(r) == 2)

    def testExternalRecordGetBySubjectOrg(self):
        '''
        Try getting ExternalRecords by Subject organization ID and their
        organization subject id (aka MRN)
        '''
        r = self.er_rh.get(subject_org=self.s1.organization_id,
                           subject_org_id=self.s1.organization_subject_id)
        self.assertTrue(len(r) == 2)

    def testExternalRecordGetByPath(self):
        '''
        Try getting ExternalRecords by path
        '''
        r = self.er_rh.get(path=self.path1)
        self.assertTrue(len(r) == 1)

    def testExternalRecordUpdateMulti(self):
        '''
        Try updating multiple records
        '''
        self.er1.record_id = 'testrecid000x'
        self.er2.record_id = 'testrecid000y'

        r = self.er_rh.update(self.er1, self.er2)
        self.assertTrue(r[0].get('success'))
        self.assertTrue(r[1].get('success'))

    def testExternalRecordUpdateBadId(self):
        '''
        Try updating an ExternalRecord with the ID of an existing record.
        Expect this to fail.
        '''
        self.er2.record_id = self.er1.record_id
        self.er2.path = self.er1.path
        r = self.er_rh.update(self.er2)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1, 'Exactly one error was expected')
        self.assertTrue(errors[0] == ErrorConstants.ERROR_RECORD_ID_ALREADY_IN_EXTERNAL_SYSTEM)

    def testExternalRecordUpdateNoRecord(self):
        '''
        Try to update an ExternalRecord that does not exist. Expect this to fail.
        '''
        self.er2.id = -1
        r = self.er_rh.update(self.er2)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors), 'Exactly one error was expected')
        self.assertTrue(errors[0] == ErrorConstants.ERROR_RECORD_ID_NOT_FOUND)

    def testExternalRecordGetById(self):
        '''
        Try to retrieve an ExternalRecord by its ID
        '''
        r = self.er_rh.get(id=self.er1.id)
        self.assertTrue(r.id == self.er1.id)

    def testExternalRecordGetLinksById(self):
        '''
        Try to retrieve an ExternalRecord links by the primary ExternalRecord's
        ID
        '''
        r = self.er_rh.get(id=self.er1.id, links=True)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['external_record']['id'], 4)

    def testExternalRecordDeleteLinks(self):
        '''
        Try to retrieve an ExternalRecord links by the primary ExternalRecord's
        ID
        '''
        r = self.er_rh.unlink(self.er1, 1)
        self.assertTrue(json.loads(r)['success'])

    def testExternalRecordDeleteByPath(self):
        '''
        Try to delete ExternalRecords by path. Expect subsequent query to fail
        because all records have been deleted.
        '''
        self.er_rh.delete(path=self.path1)
        try:
            self.assertRaises(self.er_rh.get(path=self.path1), PageNotFound)
        except PageNotFound:
            pass

    def testExternalRecordDeleteByExternalSystem(self):
        '''
        Try to delete ExternalRecords by ExternalSystem. Expect subsequent query
        to fail because all records have been deleted.
        '''
        self.er_rh.delete(external_system_id=self.es1.id)
        try:
            self.assertRaises(
                self.es_rh.external_records(external_system_id=self.es1.id),
                PageNotFound)
        except PageNotFound:
            pass

    def testExternalRecordDeleteBySubject(self):
        '''
        Try to delete ExternalRecords by Subject. Expect subsequent query for
        records associated with that subject to fail as they have been deleted.
        '''
        self.er_rh.delete(subject_id=self.s1.id)
        try:
            self.assertRaises(
                self.es_rh.external_records(external_system_id=self.es1.id),
                PageNotFound)
        except PageNotFound:
            pass

    def testExternalRecordDeleteByExSysURL(self):
        '''
        Try to delete ExternalRecords based on an ExternalSystem's URL.
        Expect subsequent query for records associated with that ExternalSystem
        to fail as they have been deleted.
        '''
        self.er_rh.delete(external_system_url=self.es1.url)
        try:
            self.assertRaises(
                self.er_rh.get(external_system_url=self.es1.url),
                PageNotFound)
        except PageNotFound:
            pass


class TestExternalSystemHandler(ehbTestClass):

    def testExternalSystemSubjectsByID(self):
        '''
        Try getting subjects associated with an external system by that
        external systems ID.
        '''
        r = self.es_rh.subjects(external_system_id=self.es1.id)
        self.assertTrue(len(r) == 2)

    def testExternalSystemSubjectsByPath(self):
        '''
        Try getting subjects associated with an external system by path.
        '''
        r = self.es_rh.subjects(external_system_id=self.es1.id, path=self.path1)
        self.assertTrue(len(r) == 1)

    def testExternalSystemSubjectsByOrgID(self):
        '''
        Try getting subjects associated with an external system by org id.
        '''
        r = self.es_rh.subjects(external_system_id=self.es1.id,
                                organization_id=self.s1.organization_id)
        self.assertTrue(len(r) == 2)

    def testExternalSystemSubjectsByPathAndOrg(self):
        '''
        Try getting subjects associated with an external system by org id
        and path.
        '''
        r = self.es_rh.subjects(external_system_id=self.es1.id,
                                path=self.path1,
                                organization_id=self.s1.organization_id)
        self.assertTrue(len(r) == 1)
        self.assertTrue(r[0].id == self.s1.id)

    def testExternalSystemExternalRecordsByExSys(self):
        '''
        Try getting ExternalRecords associated with an external system by
        external system id.
        '''
        r = self.es_rh.external_records(external_system_id=self.es1.id)
        self.assertTrue(len(r) == 2)

    def testExternalSystemExternalRecordsByExSysPath(self):
        '''
        Try getting ExternalRecords associated with an external system by
        external system id and path.
        '''
        r = self.es_rh.external_records(external_system_id=self.es1.id,
                                        path=self.path1)
        self.assertTrue(len(r) == 1)

    def testExternalSystemExternalRecordsByExSysOrg(self):
        '''
        Try getting ExternalRecords associated with an external system by
        external system id and organization id.
        '''
        r = self.es_rh.external_records(external_system_id=self.es1.id,
                                        organization_id=self.o1.id)
        self.assertTrue(len(r) == 2)

    def testExternalSystemExternalRecordsByExSysSubject(self):
        '''
        Try getting ExternalRecords associated with an external system by
        external system id and subject id.
        '''
        r = self.es_rh.external_records(external_system_id=self.es1.id,
                                        subject_id=self.s1.id)
        self.assertTrue(len(r) == 2)

    def testExternalSystemExternalRecordsByExSysSubjectPath(self):
        '''
        Try getting ExternalRecords associated with an external system by
        external system id, subject id, and path.
        '''
        r = self.es_rh.external_records(external_system_id=self.es1.id,
                                        subject_id=self.s1.id,
                                        path=self.path1)
        self.assertTrue(len(r) == 1)

    def testExternalSystemCreate(self):
        '''
        Try creating an ExternalSystem
        '''
        es1 = ExternalSystem(name='testESNameCreate',
                             url='http://testcreate.com',
                             description="a test system")
        r = self.es_rh.create(es1)[0]
        self.assertTrue(r.get('success'))

    def testExternalSystemCreateDupe(self):
        '''
        Try creating an ExternalSystem with the same name as an existing
        ExternalSystem. Expect this to fail.
        '''
        es = ExternalSystem(name=self.es_name1, url='http://testagain.com/',
                            description="a test system")
        r = self.es_rh.create(es)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(
            errors[0] == ErrorConstants.ERROR_EXTERNAL_SYSTEM_NAME_EXISTS
        )

    def testExternalSystemCreateDupe2(self):
        '''
        Try creating an ExternalSystem with the same URL as an existing
        ExternalSystem. Expect this to fail.
        '''
        es = ExternalSystem(name='xxx', url='http://test.com/',
                            description="a test system")
        r = self.es_rh.create(es)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(
            errors[0] == ErrorConstants.ERROR_EXTERNAL_SYSTEM_URL_EXISTS
        )

    def testExternalSystemUpdate(self):
        '''
        Try updating an ExternalSystem's description. Expect success
        '''
        self.es1.description = 'This is a test system'
        r = self.es_rh.update(self.es1)[0]
        self.assertTrue(r.get('success'))

    def testExternalSystemDelete(self):
        '''
        Try deleting an ExternalSystem by id. Expect subsequent query for this
        ExternalSystem to fail.
        '''
        self.es_rh.delete(id=self.es1.id)
        try:
            self.assertRaises(self.es_rh.get(id=self.es1.id), PageNotFound)
        except PageNotFound:
            pass

    def testExternalSystemDeleteBadID(self):
        '''
        Try deleting an ExternalSystem with a non-existent ID. Expect this to
        fail.
        '''
        try:
            self.assertRaises(self.es_rh.delete(id='badid'), PageNotFound)
        except PageNotFound:
            pass

    def testExternalSystemDeleteBadName(self):
        '''
        Try deleting an ExternalSystem with a non-existent name. Expect this to
        fail.
        '''
        try:
            self.assertRaises(self.es_rh.delete(name='badname'), PageNotFound)
        except PageNotFound:
            pass

    def testExternalSystemDeleteBadUrl(self):
        '''
        Try deleting an ExternalSystem with a non-existent url. Expect this to
        fail.
        '''
        try:
            self.assertRaises(self.es_rh.delete(url='badurl'), PageNotFound)
        except PageNotFound:
            pass

    def testExternalSystemMultiCreate(self):
        '''
        Try creating multiple ExternalSystem objects at the same time
        '''
        es1 = ExternalSystem(name='ES1Multi', url='http://testest1.com', description='A test system')
        es2 = ExternalSystem(name='ES2Multi', url='http://testest2.com', description='A test system 2')
        r = self.es_rh.create(es1, es2)
        self.assertTrue(r[0].get('success') and r[1].get('success'))
        self.es_rh.delete(name='ES1Multi')
        self.es_rh.delete(name='ES2Multi')

    def testExternalSystemMultiUpdate(self):
        '''
        Try updating multiple ExternalSystem objects
        '''
        self.es1.description = 'Im new and informative'
        self.es2.description = 'Im new and exciting'
        r = self.es_rh.update(self.es1, self.es2)
        self.assertTrue(r[0].get('success') and r[1].get('success'))

    def testExternalSystemUpdateBadName(self):
        '''
        Try updating an ExternalSystem with the name of an existing ExternalSystem

        Expect this to fail
        '''
        self.es2.name = self.es1.name
        r = self.es_rh.update(self.es2)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0] == ErrorConstants.ERROR_EXTERNAL_SYSTEM_NAME_EXISTS)

    def testExternalSystemUpdateBadUrl(self):
        '''
        Try updating an ExternalSystem with the url of an existing ExternalSystem

        Expect this to fail
        '''
        self.es2.url = self.es1.url
        r = self.es_rh.update(self.es2)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0] == ErrorConstants.ERROR_EXTERNAL_SYSTEM_URL_EXISTS)

    def testExternalSystemUpdateNoES(self):
        '''
        Try updating an ExternalSystem that does not exist

        Expect this to fail
        '''
        self.es2.id = -1
        r = self.es_rh.update(self.es2)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0] == ErrorConstants.ERROR_RECORD_ID_NOT_FOUND)

    def testExternalSystemGetByID(self):
        '''
        Try to retrieve an ExternalSystem by ID
        '''
        es = self.es_rh.get(id=self.es1.id)
        self.assertTrue(es.id == self.es1.id)

    def testExternalSystemGetByName(self):
        '''
        Try to retrieve an ExternalSystem by name
        '''
        es = self.es_rh.get(name=self.es1.name)
        self.assertTrue(es.name == self.es1.name)

    def testExternalSystemGetByID(self):
        '''
        Try to retrieve an ExternalSystem by ID
        '''
        es = self.es_rh.get(id=self.es1.id)
        self.assertTrue(es.id == self.es1.id)

    def testExternalSystemGetByBadID(self):
        '''
        Try to retrieve an ExternalSystem by bad ID

        Expect this to fail.
        '''
        try:
            self.assertRaises(self.es_rh.get(id=-1), PageNotFound)
        except PageNotFound:
            pass

    def testExternalSystemGetByBadName(self):
        '''
        Try to retrieve an ExternalSystem by bad name

        Expect this to fail.
        '''
        try:
            self.assertRaises(self.es_rh.get(name='nonexistent'), PageNotFound)
        except PageNotFound:
            pass

    def testExternalSystemGetByBadUrl(self):
        '''
        Try to retrieve an ExternalSystem by bad name

        Expect this to fail.
        '''
        try:
            self.assertRaises(self.es_rh.get(url='http://example.com/bad'), PageNotFound)
        except PageNotFound:
            pass


class TestSubjectRequestHandler(ehbTestClass):

    def testSubjectCreate(self):
        '''
        Try to create a Subject
        '''
        dob = datetime.datetime.now()
        s = Subject(
            first_name='FIRST_ONE',
            last_name="LAST_ONE",
            organization_id=self.o1.id,
            organization_subject_id='123456',
            dob=dob)
        r = self.s_rh.create(s)[0]
        self.assertTrue(r.get('success'))

    def testSubjectCreateFailure(self):
        '''
        Try to create a Subject with an existing mrn. Expect this to fail.
        '''
        dob = datetime.datetime.now()
        s = Subject(
            first_name='TEST',
            last_name='ONE',
            organization_id=self.o1.id,
            organization_subject_id=self.s1.organization_subject_id,
            dob=dob
        )
        r = self.s_rh.create(s)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0] == ErrorConstants.ERROR_SUBJECT_ORG_ID_EXISTS)

    def testSubjectUpdate(self):
        '''
        Try to update a Subject
        '''
        self.s1.old_subject = self.s1
        self.s1.first_name = 'NEW NAME'
        r = self.s_rh.update(self.s1)[0]
        self.assertTrue(r.get('success'))

    def testSubjectDelete(self):
        '''
        Try to delete a Subject expect subsequent retrieval of Subject to fail
        '''
        self.s_rh.delete(id=self.s1.id)
        try:
            self.assertRaises(self.s_rh.get(id=self.s1.id), PageNotFound)
        except PageNotFound:
            pass

    def testSubjectDeleteFail(self):
        '''
        Try to delete a non-existent Subject. Expect this to throw a PageNotFound
        error.
        '''
        try:
            self.assertRaises(self.s_rh.delete(
                organization_subject_id='badid',
                organization_id=self.s1.organization_id
            ), PageNotFound)
        except PageNotFound:
            pass

    def testSubjectMultiCreate(self):
        '''
        Try to create multiple Subjects with one request.
        '''
        dob = datetime.datetime.now()
        s1 = Subject(first_name='SUBJECT', last_name="ONE",
                     organization_id=self.o1.id,
                     organization_subject_id='1111111', dob=dob)
        s2 = Subject(first_name='SUBJECT', last_name="TWO",
                     organization_id=self.o1.id,
                     organization_subject_id='2222222', dob=dob)
        r = self.s_rh.create(s1, s2)
        b = r[0].get('success') and r[1].get('success')
        self.assertTrue(b)

    def testSubjectMultiUpdate(self):
        '''
        Try to update multiple Subject records with one request.
        '''
        self.s1.old_subject = self.s1
        self.s1.first_name = 'ONE_FIRST'
        self.s2.old_subject = self.s2
        self.s2.first_name = 'TWO_FIRST'
        r = self.s_rh.update(self.s1, self.s2)
        b = r[0].get('success') and r[1].get('success')
        self.assertTrue(b)

    def testSubjectDupeOrgIdFail(self):
        '''
        Try to update an existing Subject record with the organization_subject_id
        of another Subject record. Expect this to fail
        '''
        self.s1.organization_subject_id = self.s2.organization_subject_id
        self.s1.old_subject = self.s1
        r = self.s_rh.update(self.s1)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0] == ErrorConstants.ERROR_SUBJECT_ORG_ID_EXISTS)

    def testSubjectUpdateNonExistentSubject(self):
        '''
        Try to update a non existent Subject. Expect this to fail.
        '''
        self.s1.id = -1
        self.s1.old_subject = self.s1
        r = self.s_rh.update(self.s1)[0]
        errors = r.get('errors')
        self.assertFalse(r.get('success'))
        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0] == ErrorConstants.ERROR_RECORD_ID_NOT_FOUND)

    def testSubjectGetByID(self):
        '''
        Try to retrieve a Subject object by ID
        '''
        s = self.s_rh.get(id=self.s1.id)
        self.assertTrue(s == self.s1)

    def testSubjectGetByOrgAndOrgID(self):
        '''
        Try to retrieve Subject object by combination of Org and Org Id
        '''
        s = self.s_rh.get(
            organization_id=self.s1.organization_id,
            organization_subject_id=self.s1.organization_subject_id)
        self.assertTrue(s == self.s1)

    def testSubjectGetByIDFail(self):
        '''
        Try to retrieve Subject by non-existent ID. Expect this to fail.
        '''
        try:
            self.assertRaises(self.s_rh.get(id=-1), PageNotFound)
        except PageNotFound:
            pass

    def testSubjectGetByOrgandOrgIDFail(self):
        '''
        Try to retrieve a Subject by non-existent Org ID and Organization Sub ID
        '''
        try:
            self.assertRaises(self.s_rh.get(organization_id=-1,
                                            organization_subject_id='badid'))
        except PageNotFound:
            pass


class TestGroupRequestHandler(ehbTestClass):

    def testGroupCreate(self):
        '''
        Try to create a Group
        '''
        g1 = Group(name='testgroup2', is_locking=False,
                   client_key='ck', description='A test group')
        r = self.g_rh.create(g1)[0]
        self.assertTrue(r.get('success'))

    def testGroupCreateMulti(self):
        '''
        Try to create a multiple Groups with one request
        '''
        g1 = Group(name='testgroup2', is_locking=False,
                   client_key='ck', description='A test group')
        g2 = Group(name='testgroup3', is_locking=False,
                   client_key='ck', description='Another test group')
        r = self.g_rh.create(g1, g2)
        b = r[0].get('success') and r[1].get('success')
        self.assertTrue(b)

    def testGroupHaseHBKey(self):
        '''
        A created Group should have an ehb key
        '''
        g = self.g_rh.get(name=self.g1.name)
        self.assertTrue(self.g1.ehb_key)

    def testGroupGetByID(self):
        '''
        Try to retrieve a Group by id.
        '''
        g = self.g_rh.get(id=self.g1.id)
        self.assertEqual(self.g1.id, g.id)

    def testGroupGetByName(self):
        '''
        Try to retrieve a Group by name.
        '''
        g = self.g_rh.get(name=self.g1.name)
        self.assertEqual(g.id, self.g1.id)

    def testGroupGetByIDFail(self):
        '''
        Try to retrieve a Group with a non-existent ID. Expect this to fail
        '''
        try:
            self.assertRaises(self.g_rh.get(id=-1), RequestedRangeNotSatisfiable)
        except RequestedRangeNotSatisfiable:
            pass

    def testGroupGetByNameFail(self):
        '''
        Try to retrieve a Group with a non-existent ID. Expect this to fail
        '''
        try:
            self.assertRaises(self.g_rh.get(name='badname'), RequestedRangeNotSatisfiable)
        except RequestedRangeNotSatisfiable:
            pass

    def testGroupUpdate(self):
        '''
        Try to update a group
        '''
        self.g1.current_client_key(self.g1.client_key)
        new_name = self.g1.name + 'xyz'
        self.g1.name = new_name
        r = self.g_rh.update(self.g1)[0]
        self.assertTrue(r.get('success'))

    def testGroupAddSubjects(self):
        '''
        Try to add subjects to a Group.
        '''
        r = self.g_rh.add_subjects(self.g1, [self.s2])[0]
        self.assertTrue(r.get('success'))

    def testGroupGetSubjects(self):
        '''
        Try to retrieve Subjects from a Group.
        '''
        r = self.g_rh.get_subjects(self.g1)
        self.assertEqual(r[0], self.s1)
        self.assertEqual(len(r), 1)

    def testGroupRemoveSubjects(self):
        '''
        Try to remove a Subject from a Group.
        '''
        self.g_rh.remove_subject(self.g1, self.s1)
        r = self.g_rh.get_subjects(self.g1)
        self.assertEqual(len(r), 0)

    def testGroupAddExternalRecords(self):
        '''
        Try to add an ExternalRecord to a Group.
        '''
        r = self.g_rh.add_records(self.g2, [self.er2])[0]
        self.assertTrue(r.get('success'))

    def testGroupGetExternalRecords(self):
        '''
        Try to retrieve the ExternalRecords of a Group.
        '''
        r = self.g_rh.get_records(self.g2)
        self.assertEqual(r[0].record_id, self.er1.record_id)

    def testGroupRemoveExternalRecords(self):
        '''
        Try to remove ExternalRecords from a Group.
        '''
        self.g_rh.remove_record(self.g2, self.er1)
        r = self.g_rh.get_records(self.g2)
        self.assertEqual(len(r), 0)

    def testGroupDeleteByID(self):
        '''
        Try to remove a Group by ID. Expect subsequent request for that Group to fail.
        '''
        self.g_rh.delete(id=self.g1.id, client_key=self.g1.client_key)
        try:
            self.assertRaises(self.g_rh.get(id=self.g1.id), RequestedRangeNotSatisfiable)
        except RequestedRangeNotSatisfiable:
            pass

    def testGroupDeleteByName(self):
        '''
        Try to remove a Group by name. Expect subsequent request for that Group to fail.
        '''
        self.g_rh.delete(name=self.g1.name, client_key=self.g1.client_key)
        try:
            self.assertRaises(self.g_rh.get(name=self.g1.name), RequestedRangeNotSatisfiable)
        except RequestedRangeNotSatisfiable:
            pass


class TestOrganizationRequestHandler(ehbTestClass):

    def testOrganizationCreate(self):
        '''
        Try to create an Organization.
        '''
        o = Organization(name='testorg99', subject_id_label='subject')
        r = self.o_rh.create(o)[0]
        self.assertTrue(r.get('success'))

    def testOrganizationCreateMulti(self):
        '''
        Try to create multiple Organizations with one request.
        '''
        pass

    def testOrganizationCreateFailDupe(self):
        '''
        Try to create an Organization with a duplicate name. Expect this to fail.
        '''
        pass

    def testOrganizationUpdate(self):
        '''
        Try to update the subject_id_label of an Organization
        '''
        pass

    def testOrganizationDelete(self):
        '''
        Try to delete an Organization. Expect subsequent request for that
        Organization to fail.
        '''
        pass
