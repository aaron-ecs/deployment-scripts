"""
Test class for deploying to EC2.
"""
import sys
import unittest
from unittest.mock import patch
from io import StringIO

from botocore.exceptions import ClientError

import deploy_to_ec2


class DeployToEC2Test(unittest.TestCase):
    """
    Test class for deploying to EC2.
    """

    @patch('deploy_to_ec2.open_connection')
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
            deploy_to_ec2.deploy_to_ec2('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Unable to open a connection to codedeploy' in output

    @patch('deploy_to_ec2.deploy_artifact')
    def test_start_deployment_error(self, mock_boto3):
        """ Test for exit code and logging if deployment does not start """
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
            deploy_to_ec2.deploy_to_ec2('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Error when starting deployment' in output

    @patch('deploy_to_ec2.deploy_artifact')
    @patch('deploy_to_ec2.get_deployment_status', return_value="Succeeded")
    def test_deployment_succeeded(self, deploy_artifact, get_status):
        """ Test for exit code and logging if deployment runs okay """
        # GIVEN
        sys.stdout = StringIO()
        deploy_artifact.return_json = "Succeeded"
        get_status.return_value = "Succeeded"

        # WHEN
        with self.assertRaises(SystemExit):
            deploy_to_ec2.deploy_to_ec2('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Deployment is a success' in output

    @patch('deploy_to_ec2.deploy_artifact')
    @patch('deploy_to_ec2.get_deployment_status', return_value="Failed")
    def test_deployment_failed(self, deploy_artifact, get_status):
        """ Test for exit code and logging if deployment fails """
        # GIVEN
        sys.stdout = StringIO()
        deploy_artifact.return_json = "Failed"
        get_status.return_value = "Failed"

        # WHEN
        with self.assertRaises(SystemExit):
            deploy_to_ec2.deploy_to_ec2('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Deployment has failed!' in output

    @patch('deploy_to_ec2.deploy_artifact')
    @patch('deploy_to_ec2.get_deployment_status', return_value="Stopped")
    def test_deployment_stopped(self, deploy_artifact, get_status):
        """ Test for exit code and logging if deployment is stopped """
        # GIVEN
        sys.stdout = StringIO()
        deploy_artifact.return_json = "Stopped"
        get_status.return_value = "Stopped"

        # WHEN
        with self.assertRaises(SystemExit):
            deploy_to_ec2.deploy_to_ec2('', '', '')
        output = sys.stdout.getvalue().strip()

        # THEN
        assert 'Deployment has failed!' in output
