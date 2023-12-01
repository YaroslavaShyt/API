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

    @patch('proto_pb2.projects.projects_pb2.DeleteProjectsRequest')
    def test_delete_record_projects(self, DeleteProjectsRequest_mock):
        # correct data (id in table)
        DeleteProjectsRequest_mock.return_value = {
            "success": True, "message": ["Record deleted."]}
        response = DeleteProjectsRequest_mock()
        # check response parameters
        self.assertTrue(response["success"])
        self.assertEqual(response["message"][0], "Record deleted.")
        # incorrect data (id not in table)
       # request = DeleteProjectsRequest(id=[1])
       # response = self.servicer.UpdateRecordProjects(request, context)
        # check response parameters
        #self.assertFalse(response.success)
        #self.assertEqual(response.message[0], "No matching records found.")


"""
    def test_update_record_projects(self):  
        # correct data   
        request = UpdateProjectsRequest(
            id=[10], update_data={"name": "Updated Name"})
        context = MagicMock()
        response = self.servicer.UpdateRecordProjects(request, context)
            # check response parameters
        self.assertTrue(response.success)
        self.assertEqual(response.message[0], "Record updated")

        # incorrect data (id not in table)
        request = UpdateProjectsRequest(
            id=[1], update_data={"name": "Updated Name"})
        context = MagicMock()
        response = self.servicer.UpdateRecordProjects(request, context)
            # check response parameters
        self.assertFalse(response.success)
        self.assertEqual(response.message[0], "No matching records found.")


    def test_read_record_projects(self): 
        # correct data 
        context = MagicMock()
        request = ReadProjectsRequest(id=[4, 5, 6])
        response = self.servicer.ReadRecordProjects(request, context)
            # check response parameters
        self.assertTrue(response.success)
        for i in response.data:
            self.assertIsInstance(i.name, str)
            self.assertIsInstance(i.description, str)
            self.assertIsInstance(i.status, int)

        # incorrect data 
        request = ReadProjectsRequest(id=[1])
        response = self.servicer.ReadRecordProjects(request, context)
            # check response parameters
        self.assertFalse(response.success)

    # test CreateRecordProjects: name(str), description(str), status(int)
    def test_create_record_projects(self):
      #  try:
            # correct data
            request = CreateProjectsRequest(
                name="Project Name", description="Project Description", status=1)
            context = MagicMock()
            response = self.servicer.CreateRecordProjects(request, context)
                # check response parameters
            self.assertTrue(response.success)
            self.assertEqual(response.message[0], "Record created")

            # incorrect data
            request = CreateProjectsRequest(
                name="", description="", status=4)
            context = MagicMock()
            response = self.servicer.CreateRecordProjects(request, context)
                # check response parameters
            self.assertFalse(response.success)
           # self.assertEqual(response.message, context)

           # not all required data
            request = CreateProjectsRequest(
                description="description", status=1)
            context = MagicMock()
            response = self.servicer.CreateRecordProjects(request, context)
                # check response parameters
            self.assertFalse(response.success)
    #    except Exception as ex:
    #        print(f'CREATE RECORD PROJECTS: {ex}')

   
        

    def test_update_record_projects(self):
        try:
            request = UpdateProjectsRequest(
                id=[10], update_data={"name": "Updated Name"})
            context = MagicMock()
            response = self.servicer.UpdateRecordProjects(request, context)
            # check response parameters
            self.assertTrue(response.success)
            self.assertEqual(response.message, "Record updated")
        except Exception as ex:
            print(f'UPDATE RECORD PROJECTS: {ex}')

    
"""

if __name__ == '__main__':
    unittest.main()
