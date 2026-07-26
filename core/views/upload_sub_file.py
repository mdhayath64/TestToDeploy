from rest_framework.views import APIView

from core.service.sub_background_img import SubBackgroundImg
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class UploadSubFileView(APIView,ApiFramework):

    serializer=None
    method=None
    def process(self):
        service=SubBackgroundImg()
        if self.method=='POST':
            sub_icon = self.files.get('file') if self.files else None
            if sub_icon:
                self.data['file'] = sub_icon

                return service.upload_background_img(self.data)

            return custom_response_obj(message='file is required', code=400)
        else:
            return service.get_img()

    def post(self, request):
        self.data = request.data
        self.files = request.FILES  # Store files separately
        self.method = "POST"
        return self.main()


    def get(self,request):
        return self.main()