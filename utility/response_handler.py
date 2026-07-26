from rest_framework import status
from rest_framework.response import Response
from utility.common_utils import custom_response_obj


class ResponseSchema:

    def __init__(self, message,data, status_code, error_msg=None, error_code=None, **kwargs):
        self.data = data
        self.status_code = status_code
        self.__error_msg=error_msg
        self.__error_code=error_code
        self.__message=message
        self.__kwargs=kwargs

    def get_response(self):
        resp = custom_response_obj(message=self.__message,
                                   code=self.status_code,
                                   data=self.data,
                                   **self.__kwargs
                                    )
        return Response(resp, status=self.status_code)


class HttpResponse:

    def __unauthorized(self, data,message=None):
        response = ResponseSchema(data=data,status_code=status.HTTP_401_UNAUTHORIZED,message=message)
        return response.get_response()

    def __bad_request(self, data,message=None):
        response = ResponseSchema(data=data,status_code=status.HTTP_400_BAD_REQUEST,message=message)
        return response.get_response()

    def __internal_server_error(self, data,message=None):
        response = ResponseSchema(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message=message)
        return response.get_response()

    def __not_found(self, data, message=None):
        response = ResponseSchema(data=data, status_code=status.HTTP_404_NOT_FOUND, message=message)
        return response.get_response()

    def __conflict_response(self, data,message=None):
        response = ResponseSchema(data=data, status_code=status.HTTP_409_CONFLICT,message=message)
        return response.get_response()

    def __success_response(self, data, **kwargs):
        response = ResponseSchema(data=data, status_code=status.HTTP_200_OK, message='request processed successfully',
                                  **kwargs)
        return response.get_response()

    def __delete_response(self, data):
        response = ResponseSchema(data=data, status_code=status.HTTP_204_NO_CONTENT, message='data deleted successfully')
        return response.get_response()

    def __forbidden(self, data,message=None):
        response=ResponseSchema(data=data, status_code=status.HTTP_403_FORBIDDEN,message=message)
        return response.get_response()

    def response(self, code, data, message=None ,**kwargs):

        response=None
        if code in [200, 201, 204]:
            response=self.__success_response(data, **kwargs)
        elif code==400:
            response=self.__bad_request(data, message=message)
        elif code==401:
            response =self.__unauthorized(data, message=message)
        elif code==403:
            response=self.__forbidden(data)
        elif code==404:
            response=self.__not_found(data, message=message)
        elif code==409:
            response=self.__conflict_response(data)
        elif code==500:
            response=self.__internal_server_error(data,message=message)

        return response
