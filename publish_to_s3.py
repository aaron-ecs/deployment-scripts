import boto3
from botocore.exceptions import ClientError
from time import strftime
import sys

VERSION_LABEL = strftime('%Y%m%d%H%M%S')


def publish_to_s3(artifact, bucket, key):
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


