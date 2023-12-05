import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from proto_pb2.projects.projects_pb2 import CreateProjectsRequest, ReadProjectsRequest, UpdateProjectsRequest, DeleteProjectsRequest
from server_functions.servicers.projects_servicer import ProjectServicer


class TestProjectServicer(unittest.TestCase):

    # setup a test module
    def setUp(self):
        self.servicer = ProjectServicer()

    def _run_create_record_projects_test(self, test_request, expected_success):
        context = []
        response = self.servicer.CreateRecordProjects(test_request, context)
        self.assertEqual(response.success, expected_success)

    def test_create_record_projects_no_data(self):
        test_request = CreateProjectsRequest()
        self._run_create_record_projects_test(test_request, expected_success=False)

    def test_create_record_projects_not_all_data(self):
        test_request = CreateProjectsRequest(name='a')
        self._run_create_record_projects_test(test_request, expected_success=False)

    def test_create_record_projects_empty_name(self):
        test_request = CreateProjectsRequest(name='', description="Project Description", status=1)
        self._run_create_record_projects_test(test_request, expected_success=False)

    def test_create_record_projects_whitespace_name(self):
        test_request = CreateProjectsRequest(name='    ', description="Project Description", status=1)
        self._run_create_record_projects_test(test_request, expected_success=False)

    def test_create_record_projects_status_not_in_range(self):
        test_request = CreateProjectsRequest(name="Project Name", description="Project Description", status=3)
        self._run_create_record_projects_test(test_request, expected_success=False)

    def test_create_record_projects_positive_case_status_1(self):
        test_request = CreateProjectsRequest(
            name="Project Name", description="Project Description", status=1)
        self._run_create_record_projects_test(test_request, expected_success=True)

    def test_create_record_projects_positive_case_status_0(self):
        test_request = CreateProjectsRequest(
            name="Project Name", description="Project Description", status=0)
        self._run_create_record_projects_test(test_request, expected_success=True)

    """
    def _run_read_record_projects_test(self, test_request, expected_success):
        context = []
        response = self.servicer.ReadRecordProjects(test_request, context)
        self.assertEqual(response.success, expected_success)

    def test_read_record_projects_positive_case_numeric_exists(self):
        test_request = ReadProjectsRequest(id='4')
        self._run_read_record_projects_test(test_request, expected_success=True)

    def test_read_record_projects_positive_case_few_numeric_exists(self):
        test_request = ReadProjectsRequest(id='4,9,10,11')
        self._run_read_record_projects_test(test_request, expected_success=True)

    def test_read_record_projects_positive_case_string_exists(self):
        test_request = ReadProjectsRequest(name='Project Name')
        self._run_read_record_projects_test(test_request, expected_success=True)

    def test_read_record_projects_positive_case_few_string_exists(self):
        test_request = ReadProjectsRequest(name='updatedname,Project Name')
        self._run_read_record_projects_test(test_request, expected_success=True)

    def test_read_record_projects_positive_case_status_exists(self):
        test_request = ReadProjectsRequest(status='0')
        self._run_read_record_projects_test(test_request, expected_success=True)

    def test_read_record_projects_positive_case_few_status_exists(self):
        test_request = ReadProjectsRequest(status='0,1')
        self._run_read_record_projects_test(test_request, expected_success=True)

    def test_read_record_projects_positive_case_all_exists(self):
        test_request = ReadProjectsRequest()
        self._run_read_record_projects_test(test_request, expected_success=True)

    def test_read_record_projects_negative_numeric_id_not_in_db(self):
        test_request = ReadProjectsRequest(id='1'),
        self._run_read_record_projects_test(test_request, expected_success=False)

    def test_read_record_projects_negative_char_id_not_in_db(self):
        test_request = ReadProjectsRequest(id='a'),
        self._run_read_record_projects_test(test_request, expected_success=False)

    def test_read_record_projects_empty_name(self):
        test_request = ReadProjectsRequest(name='')
        self._run_read_record_projects_test(test_request, expected_success=False)

    def test_read_record_projects_whitespace_name(self):
        test_request = ReadProjectsRequest(name='    ')
        self._run_read_record_projects_test(test_request, expected_success=False)

    def test_read_record_projects_status_not_in_range(self):
        test_request = ReadProjectsRequest(status='3')
        self._run_read_record_projects_test(test_request, expected_success=False)

    def test_read_record_projects_statuses_not_in_range(self):
        test_request = ReadProjectsRequest(status='3,4,5')
        self._run_read_record_projects_test(test_request, expected_success=False)
    """
    """
    def _run_update_record_projects_test(self, test_request, expected_success):
        context = []
        response = self.servicer.UpdateRecordProjects(test_request, context)
        self.assertEqual(response.success, expected_success)

    def test_update_record_projects_correct_data(self):
        test_request = UpdateProjectsRequest(
                name="Project Name", description="Project Description", status='1', update_data={"name": "otherName"})
        self._run_update_record_projects_test(test_request, expected_success=True)

    def test_update_record_projects_no_data(self):
        test_request = UpdateProjectsRequest()
        self._run_update_record_projects_test(test_request, expected_success=False)

    def test_update_record_projects_no_update_data(self):
        test_request = UpdateProjectsRequest(name='name',)
        self._run_update_record_projects_test(test_request, expected_success=False)

    def test_update_record_projects_empty_update_data(self):
        test_request = UpdateProjectsRequest(name='name', update_data={})
        self._run_update_record_projects_test(test_request, expected_success=False)

    def test_update_record_projects_name_not_in_db(self):
        test_request = UpdateProjectsRequest(name='a', update_data={"name": "newname"})
        self._run_update_record_projects_test(test_request, expected_success=False)

    def test_update_record_projects_empty_name(self):
        test_request = UpdateProjectsRequest(name='    ', description="Project Description", status='1', update_data={"name": "newname"})
        self._run_update_record_projects_test(test_request, expected_success=False)
    """

"""       
    def test_delete_record_projects(self):
        correct_test_data = [
            # correct id           | numeric, exists
            DeleteProjectsRequest({"id": '4'}),
            # few correct ids      | numeric, exist
            DeleteProjectsRequest({"id": '4,9,10,11'}),
            # correct name         | string, exists
            DeleteProjectsRequest({"id": 'noldname'}),
            # few correct names    | string, exist
            DeleteProjectsRequest({"id": 'noldname, name'}),
            # correct desc         | string, exist
            DeleteProjectsRequest({"description": 'newdescription'}),
            # correct status       | numeric, exists
            DeleteProjectsRequest({"status": '0'}),
            # correct statuses     | numeric, exist
            DeleteProjectsRequest({"status": '0,1'}),
            # correct              | all records
            DeleteProjectsRequest(),
        ]
        incorrect_test_data = [
            # incorrect id | numeric, not exists
            DeleteProjectsRequest(id='1'),
            # incorrect id | non-numeric, not exists
            DeleteProjectsRequest(id='a'),
            # empty name   | empty string
            DeleteProjectsRequest(name=''),
            # empty name   | whitespaces only
            DeleteProjectsRequest(name='    '),
            # incorrect timestamp | non-numeric
            DeleteProjectsRequest(timestamp='a'),
            # status not in range | 2 not in (0,1)
            DeleteProjectsRequest(status='2'),
            # statuses not in range | 2,3,4 not in (0,1)
            DeleteProjectsRequest(status='2,3,4')
        ]
"""


if __name__ == '__main__':
    unittest.main()
