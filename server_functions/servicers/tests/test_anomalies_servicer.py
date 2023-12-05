import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from proto_pb2.anomalies.anomalies_pb2 import CreateAnomaliesRequest, ReadAnomaliesRequest, UpdateAnomaliesRequest, DeleteAnomaliesRequest
from server_functions.servicers.anomalies_servicer import AnomaliesServicer


class TestAnomaliesServicer(unittest.TestCase):

    def setUp(self):
        self.servicer = AnomaliesServicer()

    def _run_create_record_anomalies_test(self, test_request, expected_success):
        context = []
        response = self.servicer.CreateRecordAnomalies(test_request, context)
        self.assertEqual(response.success, expected_success)

    def test_create_record_anomalies_positive_case(self):
        test_request = CreateAnomaliesRequest(
            projectId=4,
            data="5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
            description="description",
            status=1,
            name="Test Name",
            tags="Test Tag",
            radius=10,
            scale=5,
            processedByMemberId=2
        )
        self._run_create_record_anomalies_test(
            test_request, expected_success=True)

    def test_create_record_anomalies_missing_required_field(self):
        test_request = CreateAnomaliesRequest(
            data="5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
            status=1,
            name="Test Name",
            tags="Test Tag",
            radius=10,
            scale=5,
            processedByMemberId=2
        )
        self._run_create_record_anomalies_test(
            test_request, expected_success=False)

    def test_create_record_anomalies_empty_name(self):
        test_request = CreateAnomaliesRequest(
            projectId=4,
            data="5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
            status=1,
            name="",
            tags="Test Tag",
            radius=10,
            scale=5,
            processedByMemberId=2
        )
        self._run_create_record_anomalies_test(
            test_request, expected_success=False)

    def test_create_record_anomalies_whitespaces_name(self):
        test_request = CreateAnomaliesRequest(
            projectId=4,
            data="5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
            status=1,
            name="      ",
            tags="Test Tag",
            radius=10,
            scale=5,
            processedByMemberId=2
        )
        self._run_create_record_anomalies_test(
            test_request, expected_success=False)

    def test_create_record_anomalies_negative_numeric(self):
        test_request = CreateAnomaliesRequest(
            projectId=4,
            data="5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
            status=1,
            name="name",
            tags="Test Tag",
            radius=-10,
            scale=5,
            processedByMemberId=2
        )
        self._run_create_record_anomalies_test(
            test_request, expected_success=False)

    def test_create_record_anomalies_invalid_member_id(self):
        test_request = CreateAnomaliesRequest(
            projectId=4,
            data="5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
            status=1,
            name="name",
            tags="Test Tag",
            radius=-10,
            scale=5,
            processedByMemberId=2087098988872
        )
        self._run_create_record_anomalies_test(
            test_request, expected_success=False)



    def _run_read_record_anomalies_test(self, test_request, expected_success):
        context = []
        response = self.servicer.ReadRecordAnomalies(test_request, context)
        self.assertEqual(response.success, expected_success)

    def test_read_record_anomalies_positive_case(self):
        test_request = ReadAnomaliesRequest(
            projectId='4', status='1')
        self._run_read_record_anomalies_test(test_request, expected_success=True)

    def test_read_record_anomalies_invalid_numeric_id(self):
        test_request = ReadAnomaliesRequest(
            projectId='1',)
        self._run_read_record_anomalies_test(test_request, expected_success=False)

    def test_read_record_anomalies_invalid_string_id(self):
        test_request = ReadAnomaliesRequest(
            projectId='a',)
        self._run_read_record_anomalies_test(test_request, expected_success=False)

    def test_read_record_anomalies_invalid_status(self):
        test_request = ReadAnomaliesRequest(
            projectId='1', name="Test Name", status='2')
        self._run_read_record_anomalies_test(
            test_request, expected_success=False)

    def test_read_record_anomalies_valid_statuses(self):
        test_request = ReadAnomaliesRequest(
            projectId='4', name="Test Name", status='0,1')
        self._run_read_record_anomalies_test(
            test_request, expected_success=True)



    def _run_update_record_anomalies_test(self, test_request, expected_success):
        context = []
        response = self.servicer.UpdateRecordAnomalies(test_request, context)
        self.assertEqual(response.success, expected_success)

    def test_update_record_anomalies_valid(self):
        test_request = UpdateAnomaliesRequest(
            id='1', update_data={"name": "test_name"})
        self._run_read_record_anomalies_test(
            test_request, expected_success=True)

    def test_update_record_anomalies_no_data(self):
        test_request = UpdateAnomaliesRequest()
        self._run_update_record_anomalies_test(
            test_request, expected_success=False)

    def test_update_record_anomalies_no_update_data(self):
        test_request = UpdateAnomaliesRequest(
            id='1')
        self._run_update_record_anomalies_test(
            test_request, expected_success=False)

    def test_update_record_anomalies_empty_update_data(self):
        test_request = UpdateAnomaliesRequest(
            id='1', update_data={})
        self._run_update_record_anomalies_test(
            test_request, expected_success=False)

    def test_update_record_anomalies_no_id_in_db(self):
        test_request = UpdateAnomaliesRequest(id='18726453', update_data={"name": "another name"})
        self._run_update_record_anomalies_test(
            test_request, expected_success=False)



    """
    def _run_delete_record_anomalies_test(self, test_request, expected_success):
        context = []
        response = self.servicer.UpdateRecordAnomalies(test_request, context)
        self.assertEqual(response.success, expected_success)
    """