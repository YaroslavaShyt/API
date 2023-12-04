import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from proto_pb2.projects.projects_pb2 import CreateProjectsRequest, ReadProjectsRequest, UpdateProjectsRequest, DeleteProjectsRequest
# from projects_pb2_grpc import ProjectsServiceStub
from ...projects_servicer import ProjectServicer


class TestProjectServicer(unittest.TestCase):
    # setup a test module
    def setUp(self):
        self.servicer = ProjectServicer()

    def test_create_record_projects(self):
        correct_test_data = [
            CreateProjectsRequest(
                name="Project Name", description="Project Description", status=1),
            CreateProjectsRequest(
                name="Project Name", description="Project Description", status=0),
        ]
        incorrect_test_data = [
            # no data
            CreateProjectsRequest(),
            # not all data
            CreateProjectsRequest(name='a'),
            # empty name   | empty string
            CreateProjectsRequest(
                name='', description="Project Description", status=1),
            # empty name   | whitespaces only
            CreateProjectsRequest(
                name='    ', description="Project Description", status=1),
            # status not in range | 3 not in (0,1)
            CreateProjectsRequest(
                name="Project Name", description="Project Description", status=3),
        ]
        # test positive cases
        for test in correct_test_data:
            response = self.servicer.CreateRecordProjects(test)
            # check response parameters
            self.assertTrue(response["success"])
            self.assertEqual(response["message"][0], "Record deleted")

        # test negative cases
        for test in incorrect_test_data:
            response = self.servicer.CreateRecordProjects(test)
            # check response parameters
            self.assertFalse(response.success)

    def test_read_record_projects(self):
        correct_test_data = [
            # correct id           | numeric, exists
            ReadProjectsRequest({"id": '4'}),
            # few correct ids      | numeric, exist
            ReadProjectsRequest({"id": '4,9,10,11'}),
            # correct name         | string, exists
            ReadProjectsRequest({"id": 'noldname'}),
            # few correct names    | string, exist
            ReadProjectsRequest({"id": 'noldname, name'}),
            # correct desc         | string, exist
            ReadProjectsRequest({"description": 'newdescription'}),
            # correct status       | numeric, exists
            ReadProjectsRequest({"status": '0'}),
            # correct statuses     | numeric, exist
            ReadProjectsRequest({"status": '0,1'}),
            # correct              | all records
            ReadProjectsRequest(),
        ]
        incorrect_test_data = [
            # incorrect id | numeric, not exists
            ReadProjectsRequest(id='1'),
            # incorrect id | non-numeric, not exists
            ReadProjectsRequest(id='a'),
            # empty name   | empty string
            ReadProjectsRequest(name=''),
            # empty name   | whitespaces only
            ReadProjectsRequest(name='    '),
            # incorrect timestamp | non-numeric
            ReadProjectsRequest(timestamp='a'),
            # status not in range | 2 not in (0,1)
            ReadProjectsRequest(status='2'),
            # statuses not in range | 2,3,4 not in (0,1)
            ReadProjectsRequest(status='2,3,4')
        ]

        # test positive cases
        for test in correct_test_data:
            response = self.servicer.ReadRecordProjects(test)
            # check response parameters
            self.assertTrue(response["success"])
            self.assertEqual(response["message"][0], "Record updated")

        # test negative cases
        for test in incorrect_test_data:
            response = self.servicer.ReadRecordProjects(test)
            # check response parameters
            self.assertFalse(response.success)

    def test_update_record_projects(self):
        correct_conditions = [
            UpdateProjectsRequest(
                name="Project Name", description="Project Description", status=1),
            UpdateProjectsRequest(
                name="Project Name", description="Project Description", status=0),
        ]
        incorrect_conditions = [
            # no data
            UpdateProjectsRequest(),
            # no update data parameter
            UpdateProjectsRequest(name='name',),
            # no update data
            UpdateProjectsRequest(name='name', update_data={}),
            # name not exists
            UpdateProjectsRequest(name='a', update_data={"name": "newname"}),
            # empty name   | empty string
            UpdateProjectsRequest(
                name='', description="Project Description", status=1, update_data={"name": "newname"}),
            # empty name   | whitespaces only
            UpdateProjectsRequest(
                name='    ', description="Project Description", status=1, update_data={"name": "newname"}),
            # status not in range | 3 not in (0,1)
            UpdateProjectsRequest(status=3, update_data={"name": "newname"}),
        ]
        for test in correct_conditions:
            response = self.servicer.UpdateRecordProjects(test)
            # check response parameters
            self.assertTrue(response.success)
            self.assertEqual(response.message[0], "Record updated")

        for test in incorrect_conditions:
            response = self.servicer.UpdateRecordProjects(test)
            # check response parameters
            self.assertFalse(response.success)
       
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

        # test positive cases
        for test in correct_test_data:
            response = self.servicer.DeleteRecordProjects(test)
            # check response parameters
            self.assertTrue(response["success"])
            self.assertEqual(response["message"][0], "Record deleted.")

         # test negative cases
        for test in incorrect_test_data:
            response = self.servicer.DeleteRecordProjects(test)
            # check response parameters
            self.assertFalse(response.success)
            self.assertEqual(response.message[0], "No matching records found.")


""" 
"""

if __name__ == '__main__':
    unittest.main()
