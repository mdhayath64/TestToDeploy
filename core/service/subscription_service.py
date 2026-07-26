import os

from core.serializers.subscription_serializer import SubscriptionSerializer
from utility.common_utils import custom_response_obj
from utility.crud_helper import CrudHelper
from utility.env_setup import environment
from utility.upload_s3 import S3Uploader


class SubscriptionPlan:
    __subscription_crud_helper=CrudHelper(SubscriptionSerializer)

    def create(self, data):
        sub_icon = data.get('sub_icon')
        _, file_extension = os.path.splitext(sub_icon.name)

        s3_key = f"subscription_icons/{data['name']}{file_extension}"

        result,upload_sub_icon_url=S3Uploader(aws_access_key_id=environment.AWS_ACCESS_KEY,
                                   aws_secret_access_key=environment.AWS_SECRET_KEY).upload_file(file_obj=sub_icon,
                                                 bucket_name=environment.AWS_BUCKET_NAME,
                                                 s3_key=s3_key,
                                                 extra_args={
                                                'ContentType': sub_icon.content_type,
                                                'ACL': 'public-read'  # If you want the file to be publicly accessible
                                            })

        if result:
            data['sub_icon']=upload_sub_icon_url
            return self.__subscription_crud_helper.add_obj(data)
        return custom_response_obj(message="failed to upload image", code=500)
    def update(self,data):
        sub_icon = data.get('sub_icon')
        if not isinstance(sub_icon, str):
            _, file_extension = os.path.splitext(sub_icon.name)

            s3_key = f"subscription_icons/{data['name']}{file_extension}"
            if sub_icon is not None and len(sub_icon)>0:
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
                    data['sub_icon'] = upload_sub_icon_url
            else:
                return custom_response_obj(message="failed to upload image", code=500)

        return self.__subscription_crud_helper.update_obj(data,update_key_value=data.get("plan_id"))

    def list(self):
        return self.__subscription_crud_helper.get_all_data()

    def retrieve(self, subscription_id):
        return self.__subscription_crud_helper.get_data_by_id(subscription_id)

    def delete(self, subscription_id):
        return self.__subscription_crud_helper.delete_obj(subscription_id)