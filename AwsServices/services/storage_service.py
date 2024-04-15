import boto3
import logging

logging.basicConfig(level=logging.INFO, filename='app.log')
logger = logging.getLogger()


class StorageService:
    def __init__(self, storage_location, aws_key, aws_secret_key):
        """
        It is taking the storage location as an argument and initializing the boto3 client
        """
        self.client = boto3.client('s3', aws_access_key_id=aws_key,
                                   aws_secret_access_key=aws_secret_key)
        self.bucket_name = storage_location

    def create_bucket(self, bucket_name):
        """
        It is creating a bucket in the storage service
        """
        try:
            self.client.create_bucket(Bucket=bucket_name)
        except Exception as e:
            logging.error(e)
            print(e)
            return False
        return True

    def bucket_exists(self, bucket_name):
        """
        It is checking if the bucket exists or not
        """
        try:
            response = self.client.list_buckets()
            for bucket in response['Buckets']:
                if bucket['Name'] == bucket_name:
                    return True
            return False
        except Exception as e:
            logging.error(e)
            print(e)
            return False

    def get_storage_location(self):
        return self.bucket_name

    def upload_file(self, file_bytes, file_name):
        """
        Uploads a file to the storage service
        It is using the bucket name where the image needs to be uploaded
        getting the file_bytes (maybe pixels) from the request and the file_name
        """
        try:
            self.client.put_object(Bucket=self.bucket_name,
                                   Body=file_bytes,
                                   Key=file_name)
        except Exception as e:
            logging.error(e)
            print(e)
            return False
        # using the put_object method to upload the file - method from boto3

        return {'fileId': file_name,
                'fileUrl': "http://" + self.bucket_name + ".s3.amazonaws.com/" + file_name}
