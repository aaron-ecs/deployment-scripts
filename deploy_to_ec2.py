"""
This module deploys a .zip artifact from AWS S3 bucket aaron-codedeploy-bucket to an EC2 instance.

Example:
    On a Jenkins master branch pipeline job following a publishing an artifact this script
    can be ran to push the code to a live application.

    $ python deploy_to_ec2.py application_name deployment_group_name s3-bucket/key

Attributes:
    app_name (str): EC2 instance name
    group_name (str): CodeDeploy deployment group name
    key (str): AWS S3 bucket key (E.G. directory/file_name.zip
"""
import sys
import boto3
from botocore.exceptions import ClientError


def deploy_new_revision(app_name, group_name, key):
    """ Main function of script to deploy the code and check response """
    try:
        code_deploy_client = boto3.client('codedeploy')
    except ClientError as err:
        print(err)
        sys.exit(1)
    try:
        response = code_deploy_client.create_deployment(
            applicationName=app_name,
            deploymentGroupName=group_name,
            revision={
                'revisionType': 'S3',
                's3Location': {
                    'bucket': 'aaron-codedeploy-bucket',
                    'key': key,
                    'bundleType': 'zip'
                }
            },
            deploymentConfigName='CodeDeployDefault.OneAtATime',
            description='Jenkins deployment',
            ignoreApplicationStopFailures=True
        )
    except ClientError as err:
        print(err)
        sys.exit(1)

    while 1:
        try:
            deploy_response = code_deploy_client.get_deployment(
                deploymentId=str(response['deploymentId'])
            )
            deploy_status = deploy_response['deploymentInfo']['status']
            if deploy_status == 'Succeeded':
                sys.exit(0)
            elif deploy_status in ('Failed', 'Stopped'):
                print('Deployment has failed!')
                sys.exit(1)
            elif deploy_status in ('InProgress', 'Queued', 'Created'):
                continue
        except ClientError as err:
            print(err)
            sys.exit(1)


if __name__ == "__main__":
    deploy_new_revision(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3]
    )
