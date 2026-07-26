import os
import uuid

from core.models import AddSubscriptionBackground
from core.serializers.subscription_serializer import AddSubscriptionBackgroundSerializer
from utility.common_utils import custom_response_obj
from utility.env_setup import environment
from utility.upload_s3 import S3Uploader


class SubBackgroundImg:

    def upload_background_img(self, data):
        sub_icon = data.get('file')
        _, file_extension = os.path.splitext(sub_icon.name)

        s3_key = f"subscription_background/background{file_extension}"

        result, upload_sub_icon_url = S3Uploader(aws_access_key_id=environment.AWS_ACCESS_KEY,
                                                 aws_secret_access_key=environment.AWS_SECRET_KEY).upload_file(
            file_obj=sub_icon,
            bucket_name=environment.AWS_BUCKET_NAME,
            s3_key=s3_key,
            extra_args={
                'ContentType': sub_icon.content_type,
                'ACL': 'public-read'  # If you want the file to be publicly accessible
            })

        if result:
            name=AddSubscriptionBackground.objects.all().first()
            if name:
                name.file_url=upload_sub_icon_url
                name.save()
            else:
                name=AddSubscriptionBackground(file_id=uuid.uuid4(), file_url=upload_sub_icon_url)
                name.save()
            name = AddSubscriptionBackground.objects.all().first()

            return custom_response_obj(data=AddSubscriptionBackgroundSerializer(name, many=False).data)

    def get_img(self):
        name = AddSubscriptionBackground.objects.all()

        return custom_response_obj(data=AddSubscriptionBackgroundSerializer(name, many=True).data)