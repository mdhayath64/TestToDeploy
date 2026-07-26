from kombu.asynchronous.http import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from core.service.subscription_service import SubscriptionPlan
from middlewares.admin_permission import IsAdmin
from utility.api_framework import ApiFramework
from utility.common_utils import custom_response_obj


class SubscriptionServiceView(APIView, ApiFramework):
    serializer = None
    permission_classes = [IsAdmin]
    parser_classes = (MultiPartParser, FormParser)  # Add support for file uploads

    def process(self):
        subscription_service = SubscriptionPlan()

        if self.method == "POST":
            # Handle file upload along with other data
            sub_icon = self.files.get('sub_icon') if self.files else None
            if sub_icon:
                self.data['sub_icon'] = sub_icon
            return subscription_service.create(self.data)
        elif self.method == "GET":
            return subscription_service.list()
        elif self.method == "RETRIEVE":
            return subscription_service.retrieve(self.data)
        elif self.method == "PATCH":
            # Handle file update if provided
            sub_icon = self.files.get('sub_icon') if self.files else None
            if sub_icon:
                self.data['sub_icon'] = sub_icon
            return subscription_service.update(self.data)
        elif self.method == "DELETE":
            return subscription_service.delete(self.data)

    def get(self, request):
        self.data = request.GET.get("subscription_id")
        if self.data:
            self.method = "RETRIEVE"
        else:
            self.method = "GET"
        return self.main()

    def post(self, request):
        self.data = request.data
        self.files = request.FILES  # Store files separately
        self.method = "POST"
        return self.main()

    def patch(self, request):
        self.data = request.data
        self.files = request.FILES  # Store files separately
        self.method = "PATCH"
        return self.main()

    def delete(self, request):
        self.data = request.GET.get("subscription_id")
        if self.data is None:
            message = custom_response_obj(message="Please include subscription_id in query param")
            return Response(data=message, status=400)
        self.method = "DELETE"
        return self.main()