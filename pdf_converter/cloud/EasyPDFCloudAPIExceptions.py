import http.client


# Used to handle all HTTP related exceptions in the API.
class EasyPDFCloudHTTPException(http.client.HTTPException):
    def __init__(self, status_code, reason, error, error_desc):
        super().__init__()
        self.__reason__ = reason
        self.__status_code__ = status_code
        self.__error__ = error
        self.__error_description__ = error_desc

    def get_reason(self):
        return self.__reason__

    def get_status_code(self):
        return self.__status_code__

    def get_error(self):
        return self.__error__

    def get_error_description(self):
        return self.__error_description__

    def set_reason(self, reason):
        self.__reason__ = reason

    def set_status_code(self, status_code):
        self.__status_code__ = status_code

    def set_error(self, error):
        self.__error__ = error

    def set_error_description(self, error_description):
        self.__error_description__ = error_description

    def __str__(self):
        return str(self.__status_code__) + ": " + self.__reason__ + ". Error: " + self.__error__ \
               + " Description/Source: " + self.__error_description__


# Used to handle all invalid arguments passed to functions in the API.
class EasyPDFCloudArgException(Exception):
    def __init__(self, param=None, arg1=None, arg2=None):
        super().__init__()
        self.__param__ = param
        self.__arg1__ = arg1
        self.__arg2__ = arg2

    def get_param(self):
        return self.__param__

    def get_arg1(self):
        return self.__arg1__

    def get_arg2(self):
        return self.__arg2__

    def __str__(self):
        if self.__param__ is not None and self.__arg1__ is not None and self.__arg2__ is not None:
            return "Invalid argument (" + self.__param__ + "). Should specify either " + "\"" + self.__arg1__ \
                   + "\" or " + "\"" + self.__arg2__ + "\"."
        elif self.__param__ is not None:
            return "Argument improperly specified/not found (" + self.__param__ + "). Update Properties.xml and try again."
        else:
            return "Probable error in Properties.xml. Missing or extraneous entry tags. Update Properties.xml and try again."