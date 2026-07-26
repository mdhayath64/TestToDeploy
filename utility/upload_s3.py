import traceback
import boto3
from botocore.exceptions import ClientError


class S3Uploader:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name='ap-south-1'):
        """
        Initialize S3 client with AWS credentials
        """
        self.region_name = region_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def get_s3_url(self, bucket_name, s3_key):
        """
        Generate the S3 URL for the uploaded file
        """
        url = f"https://{bucket_name}.s3.{self.region_name}.amazonaws.com/{s3_key}"
        return url

    def upload_file(self, file_obj, bucket_name, s3_key=None, extra_args=None):
        """
        Upload a file to S3 bucket and return the URL
        Args:
            file_obj: File object from request.FILES
            bucket_name: S3 bucket name
            s3_key: Custom key for S3 object
            extra_args: Additional arguments for S3 upload

        Returns:
            tuple: (bool, str) - (success status, URL if successful or error message if failed)
        """
        try:
            if s3_key is None:
                s3_key = file_obj.name

            if extra_args is None:
                extra_args = {}

            # Upload the file directly from the file object
            self.s3_client.upload_fileobj(
                file_obj,
                bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )

            # Generate the URL
            url = self.get_s3_url(bucket_name, s3_key)
            return True, url

        except ClientError as e:
            traceback.print_exc()
            error_message = str(e)
            return False, error_message