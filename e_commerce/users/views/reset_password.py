from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from e_commerce.users.service.user_service import UserService
from utility.api_framework import ApiFramework

class ResetPasswordView(APIView, ApiFramework):

    permission_classes = [AllowAny, ]
    serializer=None
    data=None

    def process(self):
        if self.method=="POST":
            return UserService().request_otp(email=self.data['email'])
        elif self.method=="PATCH":
            return UserService().reset_password(otp=self.data['otp'],email=self.data['email'], password=self.data['password'])

    def post(self, request):
        self.data=request.data

        self.method="POST"

        return self.main()

    def patch(self, request):
        self.data = request.data

        self.method = "PATCH"

        return self.main()