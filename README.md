# Deployment Scripts

## Usage and Setup
Intended use for the scripts is to run on CI. 

Currently there is a requirement for Python to be installed and the AWS provider chain to have credentials configured.

## Scripts

### Publish to S3
Compress your project into a `.zip` file to publish to an S3 bucket.

`$ python publish_to_s3.py your-s3-bucket your-key-name.zip`

Note: you can use this script generically but if you intend to use the `deploy_to_ec2.py` script you need to ensure you use `.zip` file extension and keep it on the key.

### Deploy to EC2
Compress your project as `artifact.zip` and run the script with the command below. The final argument can be any key you wish for your artifact name E.G. a Jenkins build number. 

Be sure you keep the `.zip` file extension.

`$ python deploy_to_ec2.py application-name code-deploy-group bucket-directory/file-name.zip`