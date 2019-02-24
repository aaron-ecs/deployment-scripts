"""
Test class for publishing an artifact to S3 bucket.
"""
import sys
from unittest.mock import patch
import unittest
from io import StringIO

from botocore.exceptions import ClientError

import publish_to_s3


class PublishToS3Test(unittest.TestCase):
    """
    Test class for publishing an artifact to S3 bucket.
    """

    @patch('publish_to_s3.open_connection')
    def test_connection_error(self, mock_boto3):
        """ Test for exit code and logging if connection to AWS fails """
        # GIVEN
        sys.stdout = StringIO()
        mock_boto3.side_effect = ClientError(
            {
                "Error": {
                    "Code": "MockedException"
                }
            }, 'MockedOperation')

        # WHEN
        with self.assertRaises(SystemExit):
            publish_to_s3.publish_to_s3('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Unable to open a connection to S3' in output

    @patch('publish_to_s3.upload_file')
    def test_upload_error(self, mock_boto3):
        """ Test for exit code and logging we upload fails """
        # GIVEN
        sys.stdout = StringIO()
        mock_boto3.side_effect = ClientError(
            {
                "Error": {
                    "Code": "MockedException"
                }
            }, 'MockedOperation')

        # WHEN
        with self.assertRaises(SystemExit):
            publish_to_s3.publish_to_s3('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Unable to upload file to the bucket' in output

    @staticmethod
    @patch('publish_to_s3.upload_file')
    def test_successful_upload(mock_boto3):
        """ Test for success and logging for happy path """
        # GIVEN
        sys.stdout = StringIO()
        mock_boto3.return_value = True

        # WHEN
        publish_to_s3.publish_to_s3('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'File was uploaded successfully' in output

    @patch('publish_to_s3.upload_file')
    def test_file_not_found_error(self, mock_boto3):
        """ Test for exit code and logging if the artifact.zip file cannot be found """
        # GIVEN
        sys.stdout = StringIO()
        mock_boto3.side_effect = IOError({'Error': {'Code': 'MockedException'}}, 'MockedOperation')

        # WHEN
        with self.assertRaises(SystemExit):
            publish_to_s3.publish_to_s3('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Unable to find artifact.zip in directory' in output
