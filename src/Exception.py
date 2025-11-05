import sys
from src.Logger import logger

def get_error_details(error,error_details:sys)->str:
    'this function will return details of error in string format, like file_name, line_number and whats the error '
    _,_,exc_tb=error_details.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))
    return error_message

class CustomException(Exception):
    def __init__(self,error,error_details:sys):
        super().__init__(error)
        self.error_message=get_error_details(error,error_details)
        logger.error(self.error_message)

    def __str__(self):
        return self.error_message

