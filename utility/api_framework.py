import json
import traceback
from abc import abstractmethod
from django.core.exceptions import ObjectDoesNotExist
import logging
from utility.common_utils import normalize_serializer_error
from utility.custom_decoder import CustomJSONEncoder
from utility.response_handler import HttpResponse

logger = logging.getLogger(__name__)

"""
    This class can be used as an abstract class for all the APIViews which have common flow of
    serializer check and try/except block. It helps improve readability and maintaining the code
    code flow:it contains of main method with format_request, run_logic, process

            1. first format request is called
            2. then run_logic is called
            3. then process return final result to main method
"""


class ApiFramework:

    def __init__(self, serializer_class=None, data=None):
        self.serializer = serializer_class
        self.__data=data

    def main(self):
        """
            this is the main method of this class, it returns the final result as instance of Response class
            with help of custom Http response class.
        """
        response = ''
        try:
            if self.serializer is None or self.serializer.is_valid():
                self.format_request()
                self.run_logic()
                data = self.process()
                status_code = data.get('status_code', 200)
                result = data.get('data')
                message = data.get('message')
                count=data.get('count')
                previous=data.get('prev')
                next=data.get('next')
                response = HttpResponse().response(code=status_code,
                                                   data=result,
                                                   message=message,
                                                   count=count, previous=previous, next=next)
            else:
                serializer_error = normalize_serializer_error(self.serializer.errors.items())
                response = HttpResponse().response(code=400, data=serializer_error,message=serializer_error)

        except ObjectDoesNotExist:
            response=HttpResponse().response(code=404,data=None,message='requested data not found')
            if self.__data is not None:
                log_data=json.dumps(self.__data, default=CustomJSONEncoder)
                logger.debug(f'Object not found for {json.dumps(log_data)}')
            else:
                logger.debug(f'Data not found')
        except Exception as e:
            traceback.print_exc()
            logger.exception('Exception ' + str(e))
            response=HttpResponse().response(code=500,data=None,message=f'internal error {str(e)}')
        return response

    @abstractmethod
    def format_request(self):
        """
            custom request formatting if required
        """
        pass

    @abstractmethod
    def run_logic(self):
        """
            custom logic of the API
        """
        pass

    @abstractmethod
    def process(self):
        """
            must return the response to the main methodI
        """
        pass