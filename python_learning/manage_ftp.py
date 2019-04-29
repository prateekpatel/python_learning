import pysftp
import datetime
import boto3
import botocore



def file_upload(filename='',bucket_name=''):
    # Create an S3 client
    s3 = boto3.client('s3')
    filename = filename
    bucket_name = bucket_name
    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(filename, bucket_name, filename)


def s3_pem_download():
    BUCKET_NAME = 'my-bucket'  # replace with your bucket name
    KEY = 'my_image_in_s3.jpg'  # replace with your object key

    s3 = boto3.resource('s3')

    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, 'my_local_image.jpg')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise



def download_file(file_path, bucket_name):
    host = "sftp.data.twosigmaiq.com"  # hard-coded
    private_key = "blackboard_rsa"  # hard-coded
    username = "blackboard"
    file_name = "prod-red_" + datetime.datetime.now().strftime('%Y-%m-%d') + "_export.zip"
    file_path = file_path + file_name
    local_path = "/Users/ppr3gim/My_workspace/o_j/local/" + file_name
    print(file_path)

    # private_key = "~/.ssh/your-key.pem"  # can use password keyword in Connection instead
    srv = pysftp.Connection(host=host, username=username, private_key=private_key)
    try:
        # srv.chdir(file_path)  # change directory on remote server
        if srv.isfile(file_path):
            srv.get(file_path)  # To download a file, replace put with get
            file_upload(file_name, bucket_name=bucket_name)
    except FileNotFoundError as e:
        print("there is no file with name %s in path %s " % (file_name, file_path))
    finally:
        srv.close()  # Close connection


download_file('/outgoing/cloverleaf/')
