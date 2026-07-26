from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Storage(S3Boto3Storage):
    location = "blogsmedia/static"


class MediaRootS3Storage(S3Boto3Storage):
    location = ""
