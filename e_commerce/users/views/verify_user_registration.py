from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from e_commerce.users.service.user_service import UserService
from utility.api_framework import ApiFramework
from utility.env_setup import environment


class VerifyUserView(APIView, ApiFramework):
    permission_classes = [AllowAny, ]
    data=None
    serializer=None
    def process(self):
        if self.method=="POST":
            return UserService().request_otp(email=self.data['email'], check_user=False)
        elif self.method=="PATCH":
            return UserService().verify_user_registration(otp=self.data['otp'],email=self.data['email'])

    def post(self, request):
        self.data=request.data
        print(request.user.is_superuser)
        if request.data.get('phone','')==environment.DJANGO_SUPERUSER_PHONE:
            self.data={'email':'tradestreak13@gmail.com'}
        print(self.data)
        self.method="POST"
        return self.main()

    def patch(self, request):
        self.data = request.data
        print(self.data)
        if request.data.get('phone','')==environment.DJANGO_SUPERUSER_PHONE:
            self.data['email']='tradestreak13@gmail.com'
        self.method = "PATCH"

        return self.main()