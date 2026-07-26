# """Created an middleware to create the ActivityLog.
# we getting proper request and response object(After processing the request)
# But there is an issue that request.user is not giving the user object even after authentication middleware runs before this middleware
# So for now I have implemented it in api framework"""
# from core_app.activity_logger.service.activity_log_service import ActivityLogService
#
#
# class ActivityLogMiddleware:
#     def __init__(self, get_response) -> None:
#         self.get_response = get_response
#
#     def __call__(self, request):
#
#         if (request.path.startswith('/admin/')):
#             response = self.get_response(request)
#             return response
#         else:
#
#             response = self.get_response(request)
#             try:
#                 ActivityLogService(request.user.id,request.path,'login',response.data).create_log()
#             except Exception:
#                 pass
#             return response
