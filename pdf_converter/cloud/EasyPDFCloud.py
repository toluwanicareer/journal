import requests
from . import EasyPDFCloudAPIExceptions


# URL Endpoints.
job_endpoint = 'https://api.easypdfcloud.com/v1/jobs/'
token_endpoint = 'https://www.easypdfcloud.com/oauth2/token'
workflow_endpoint = 'https://api.easypdfcloud.com/v1/workflows/'
authorize_endpoint = 'https://www.easypdfcloud.com/oauth2/authorize'


class EasyPDFCloudAPI():
    # Creates a token manager and loads it with a new token.
    def __init__(self, app_info, token_manager):
        self.__app_info__ = app_info
        self.__token_manager__ = token_manager
        self.__get_new_token__()

    # Checks the status codes in the HTTPResponse object and decides the appropriate action to take.
    def check_response(self, http_response, auto_refresh):
        # Indicates successful request/response.
        if 200 <= http_response.status_code < 300:
            return True

        # Request was bad or unauthorized.
        if http_response.status_code == 400 or http_response.status_code == 401:
            header = http_response.headers["WWW-Authenticate"]
            error, error_desc = "", ""
            if header is not None:
                # Get error information from the header.
                elements = self.__split_header__(header)
                for i in range(0, len(elements)):
                    name = elements[i][0].lower()
                    value = elements[i][1].replace("%20", " ")
                    if name == "error" or name == "bearer error":
                        error = value
                    elif name == "error_description" or name == "bearer error_description":
                        error_desc = value
                # If using an invalid access token, refresh it.
                if error.lower() == "\"invalid_token\"" and auto_refresh:
                    self.__get_new_token__()
                    return False
            raise EasyPDFCloudAPIExceptions.EasyPDFCloudHTTPException(http_response.status_code, http_response.reason,
                                                                      error, error_desc)

        # If a different error occurs, gathers info from the servers JSON response and raises an exception.
        try:
            json_error = http_response.json()
            e = EasyPDFCloudAPIExceptions.EasyPDFCloudHTTPException(http_response.status_code, http_response.reason,
                                                                    "N/A", "N/A")
            # Updates the exception object, if necessary.
            has_message, message = self.__has_key__(json_error, "message")
            has_error, error = self.__has_key__(json_error, "error")
            has_source, source = self.__has_key__(json_error, "source")

            if has_message:
                e.set_reason(message)
            if has_error:
                e.set_error(error)
            if has_source:
                e.set_error_description(source)
            raise e
        finally:
            pass

    @staticmethod
    # Takes a header from an HTTPResponse object and splits it into a list of its separate components.
    def __split_header__(header):
        result = []
        fields = header.split(",")
        for i in range(0, len(fields)):
            result.append(fields[i].split("="))
        return result

    @staticmethod
    # Given a JSON object, will check to see if the JSON object contains a specific key.
    def __has_key__(json_obj, key):
        try:
            k = json_obj[key]
            return True, k
        except KeyError:
            return False, None

    # Sends a POST request to the server and updates token information.
    def __get_new_token__(self):
        info = self.__app_info__.get_c_id(), self.__app_info__.get_secret()
        values = {"grant_type": "client_credentials", "client_id": info[0], "client_secret": info[1], "scope": "epc.api"}
        try:
            response = requests.post(token_endpoint, data=values)
            if self.check_response(response, False):
                json = response.json()
                if self.__has_key__(json, "refresh_token")[0]:
                    t_info = json["access_token"], json["refresh_token"], json["expires_in"], json["scope"]
                else:
                    t_info = json["access_token"], None, json["expires_in"], json["scope"]
                self.__token_manager__.set_token_info(t_info[0], t_info[1], t_info[2], scope=t_info[3])
        finally:
            pass

    # Returns a JSON object containing all the user's workflows.
    def get_workflows(self):
        token = self.__token_manager__.get_access_token()
        try:
            response = requests.get(workflow_endpoint, headers={"Authorization": "Bearer " + token})
            if self.check_response(response, True):
                return response.json()
            elif not self.check_response(response, True):
                return self.get_workflows()
        finally:
            pass

    # Returns a JSON object with information about one specific workflow.
    def get_workflow(self, workflow_id):
        token = self.__token_manager__.get_access_token()
        url = workflow_endpoint + workflow_id
        try:
            response = requests.get(url, headers={"Authorization": "Bearer " + token})
            if self.check_response(response, True):
                return response.json()
            elif not self.check_response(response, True):
                return self.get_workflow(workflow_id)
        finally:
            pass

    # Uploads a file and starts a new job.
    def new_workflow_job(self, workflow_id, file_path):
        token = self.__token_manager__.get_access_token()
        url = workflow_endpoint + workflow_id + "/jobs"
        try:
            file_obj = {'file': open(file_path, 'rb')}
            response = requests.post(url, files=file_obj, headers={"Authorization": "Bearer " + token})
            if self.check_response(response, True):
                return response.json()
            elif not self.check_response(response, True):
                return self.new_workflow_job(workflow_id, file_obj)
        finally:
            pass

    # Operation should be either "file" or "metadata". Not case sensitive.
    def start_stop_job(self, job_id, operation):
        if operation.lower() == "start" or operation.lower() == "stop":
            token = self.__token_manager__.get_access_token()
            url = job_endpoint + job_id
            try:
                response = requests.post(url, params={"operation": operation},
                                         headers={"Authorization": "Bearer " + token})
                if self.check_response(response, True):
                    return response.json()
                elif not self.check_response(response, True):
                    return self.start_stop_job(job_id, operation)
            finally:
                pass
        else:
            raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException("operation", "start", "stop")

    # Deletes a job from the server. Server WILL NOT return a JSON object.
    def delete_job(self, job_id):
        token = self.__token_manager__.get_access_token()
        url = job_endpoint + job_id
        try:
            response = requests.delete(url, headers={"Authorization": "Bearer " + token})
            if self.check_response(response, True):
                return response
            elif not self.check_response(response, True):
                return self.delete_job(job_id)
        finally:
            pass

    # Gets information about a specific job.
    def get_job_info(self, job_id):
        token = self.__token_manager__.get_access_token()
        url = job_endpoint + job_id
        try:
            response = requests.get(url, headers={"Authorization": "Bearer " + token})
            if self.check_response(response, True):
                return response.json()
            elif not self.check_response(response, True):
                return self.get_job_info(job_id)
        finally:
            pass

    # Waits for the specified job until the server indicates it has been completed.
    def wait_for_job(self, job_id):
        token = self.__token_manager__.get_access_token()
        url = job_endpoint + job_id
        try:
            response = requests.post(url, headers={"Authorization": "Bearer " + token})
            message = response.json()["message"]
            if message == "The job is already processed" or self.check_response(response, True):
                return True
            elif not self.check_response(response, True):
                return self.wait_for_job(job_id)
        except EasyPDFCloudAPIExceptions.EasyPDFCloudHTTPException as e:
            if e.get_status_code() == 409:
                return False
        finally:
            pass

    # Receives information on and downloads the output from a specific job.
    def download_job_output(self, job_id, output_type, filename=None):
        if output_type.lower() == "file" or output_type.lower() == "metadata":
            token = self.__token_manager__.get_access_token()
            if filename is None:
                url = job_endpoint + job_id + "/output/"
            else:
                url = job_endpoint + job_id + "/output/" + filename
            try:
                response = requests.get(url, params={"type": output_type}, headers={"Authorization": "Bearer " + token},
                                        stream=True)
                if self.check_response(response, True):
                    return response
                elif not self.check_response(response, True):
                    return self.download_job_output(job_id, output_type, filename)
            finally:
                pass
        else:
            raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException("file_type", "file", "metadata")
