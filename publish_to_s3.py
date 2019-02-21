"""
This module is intended to push file artifact.zip of a project to a given S3 bucket.

Example:
    On a Jenkins pipeline job following passed tests we publish the artifact for deploying later.

    $ python publish_to_s3.py s3-bucket key

Attributes:
    bucket (str): S3 bucket name
    key (str): AWS S3 bucket key (E.G. directory/file_name.zip
"""
import sys
import boto3
from botocore.exceptions import ClientError


def publish_to_s3(artifact, bucket, key):
    """ Main function of script to public the compressed project """
    try:
        s3_client = boto3.client('s3')
    except ClientError as exception:
        print(exception)
        sys.exit(1)
    try:
        s3_client.put_object(
            Body=open(artifact, 'rb'),
            Bucket=bucket,
            Key=key
        )
    except ClientError as exception:
        print(exception)
        sys.exit(1)
    except IOError as exception:
        print(exception)
        sys.exit(1)


if __name__ == "__main__":
    publish_to_s3('artifact.zip', sys.argv[1], sys.argv[2])
