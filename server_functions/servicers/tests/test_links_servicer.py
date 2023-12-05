import unittest

from unittest.mock import MagicMock
from proto_pb2.links.links_pb2 import CreateLinksRequest, ReadLinksRequest, UpdateLinksRequest, DeleteLinksRequest
from server_functions.servicers.links_servicer import LinksServicer


class TestCreateRecordLinks(unittest.TestCase):

    def setUp(self):
        self.servicer = LinksServicer()  # Замініть на ваш клас

    def test_create_record_links_success(self):
        # Prepare a valid request
        valid_request = servicer.CreateLinksRequest(
            projectId=1,
            token="example_token",
            status=1
        )

        # Mock the Session context manager to avoid actual database operations
        with unittest.mock.patch('your_module.Session') as mock_session:
            # Set up the mock session
            session_mock = MagicMock()
            mock_session.return_value.__enter__.return_value = session_mock

            # Mock the execute and commit methods
            session_mock.execute.return_value = None
            session_mock.commit.return_value = None

            # Call the method with the valid request
            response = self.servicer.CreateRecordLinks(valid_request, None)

        # Assert the success and message fields in the response
        self.assertTrue(response.success)
        self.assertEqual(response.message[0], "Record created")

    def test_create_record_links_missing_required_field(self):
        # Prepare a request with a missing required field
        invalid_request = links_pb2.CreateLinksRequest(
            token="example_token",
            status=1
        )

        # Call the method with the invalid request
        response = self.servicer.CreateRecordLinks(invalid_request, None)

        # Assert that the response indicates failure and contains an error message
        self.assertFalse(response.success)
        self.assertIn("Error: <projectId> is required", response.message[0])

    def test_create_record_links_invalid_status(self):
        # Prepare a request with an invalid status
        invalid_request = links_pb2.CreateLinksRequest(
            projectId=1,
            token="example_token",
            status=2  # Invalid status, should be 0 or 1
        )

        # Call the method with the invalid request
        response = self.servicer.CreateRecordLinks(invalid_request, None)

        # Assert that the response indicates failure and contains an error message
        self.assertFalse(response.success)
        self.assertIn("Error: <status> cannot be 2. Only allowed values - 0 or 1", response.message[0])

    # Add more test cases as needed...



if __name__ == '__main__':
    unittest.main()
