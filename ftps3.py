import datetime
import io
import logging
import os

import boto3
import botocore.exceptions
import paramiko

logger = logging.getLogger()
# logger.setLevel(os.getenv('LOGGING_LEVEL', 'DEBUG'))
logger.setLevel('DEBUG')

# read in shared properties on module load - will fail hard if any are missing
# SSH_HOST = os.environ['SSH_HOST']
SSH_HOST = "sftp.data.twosigmaiq.com"

# SSH_USERNAME = os.environ['SSH_USERNAME']
SSH_USERNAME = "blackboard"
# must have one of pwd / key - fail hard if both are missing
SSH_PASSWORD = os.getenv('SSH_PASSWORD')
# path to a private key file on S3 in 'bucket:key' format.
# SSH_PRIVATE_KEY = os.getenv('SSH_PRIVATE_KEY')
SSH_PRIVATE_KEY = 'elasticbeanstalk-us-east-1-697059505935:blackboard_rsa'
assert SSH_PASSWORD or SSH_PRIVATE_KEY, "Missing SSH_PASSWORD or SSH_PRIVATE_KEY"
# optional
# SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_PORT = 22
# SSH_DIR = os.getenv('SSH_DIR')
SSH_DIR = '/outgoing/cloverleaf/'
# filename mask used for the remote file
FILENAME = "prod-red_" + datetime.datetime.now().strftime('%Y-%m-%d') + "_export.zip"
BUCKET_NAME = 'elasticbeanstalk-us-east-1-697059505935'


def on_trigger_event(event, context):
    if SSH_PRIVATE_KEY:
        key_obj = get_private_key(*SSH_PRIVATE_KEY.split(':'))
        logging.info(key_obj)
    else:
        key_obj = None

    # prefix all logging statements - otherwise impossible to filter out in Cloudwatch
    logger.info("S3-SFTP: received trigger event")

    sftp_client, transport = connect_to_sftp(
        hostname=SSH_HOST,
        port=SSH_PORT,
        username=SSH_USERNAME,
        password=SSH_PASSWORD,
        pkey=key_obj
    )
    if SSH_DIR:
        sftp_client.chdir(SSH_DIR)
        logger.debug(f"S3-SFTP: Switched into remote SFTP upload directory")

    with transport:
        print(dir(transport))
        print(dir(sftp_client))
        print(sftp_client.getcwd())
        try:
            sftp_client.get(FILENAME, FILENAME)
            file_upload(FILENAME, BUCKET_NAME)
        except Exception as e:
            print(str(e))


def connect_to_sftp(hostname, port, username, password, pkey):
    """Connect to SFTP server and return client object."""
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password, pkey=pkey)
    client = paramiko.SFTPClient.from_transport(transport)
    logger.debug(f"S3-SFTP: Connected to remote SFTP server")
    return client, transport


def get_private_key(bucket, key):
    """
    Return an RSAKey object from a private key stored on S3.

    It will fail hard if the key cannot be read, or is invalid.

    """
    key_obj = boto3.resource('s3').Object(bucket, key)
    key_str = key_obj.get()['Body'].read().decode('utf-8')
    key = paramiko.RSAKey.from_private_key(io.StringIO(key_str))
    logger.debug(f"S3-SFTP: Retrieved private key from S3")
    return key


def file_upload(filename, bucket_name):
    # Create an S3 client
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(filename, bucket_name, filename)


