import boto3
from botocore.exceptions import ClientError
import sys


def deploy_new_revision(app_name, group_name, key):
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
            elif deploy_status == 'Failed' or deploy_status == 'Stopped' :
                print('Deployment has failed!')
            elif (deploy_status == 'InProgress') or (deploy_status == 'Queued') or (deploy_status == 'Created'):
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
