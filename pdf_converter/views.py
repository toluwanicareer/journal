from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import pdb
from .forms import UploadFileForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Token
# Create your views here.
from django.core.files.storage import FileSystemStorage
import convertapi
convertapi.api_secret = 'OzUJvmJf1jVlhO6Y'
import requests
import os.path
from .cloud import AppInfo
from .cloud import TokenInfo
from .cloud import EasyPDFCloud
from .cloud import TokenManager
from .cloud import InputProperties
from .cloud import EasyPDFCloudAPIExceptions




def __save_to_directory__(response, path):
    try:
        with open(path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except FileNotFoundError:
        print("No such file or directory: " + path)

@method_decorator(csrf_exempt, 'dispatch')
class ConvertView(View):

    def post(self, request, *args, **kwargs):
        #pdb.set_trace()
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        data = InputProperties.ImportProperties()
        data.load_properties()
        in_file = os.path.join(data.get_input_directory(), filename)#data.get_file_name())
        file_out=data.get_output_directory()
        usr_info = AppInfo.AppInfo(data.get_client_id(), data.get_client_secret())
        token_manager = TokenManager.TokenManager(TokenInfo.TokenInfo(""))
        try:
            api_test = EasyPDFCloud.EasyPDFCloudAPI(usr_info, token_manager)
        except KeyError:
            raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException("Unknown Parameter")

        # Creates a new job and uploads a file to convert.
        json_job = api_test.new_workflow_job(data.get_workflow_id(), in_file)
        print(json_job)
        try:
            # View info about the current job.
            print(api_test.get_job_info(json_job["jobID"]))

            # Wait for the job as it is being processed.
            while api_test.wait_for_job(json_job["jobID"]) is False:
                print("The job is currently running.")

            # Gives the output files name on the server.
            output = api_test.download_job_output(json_job["jobID"], "metadata").json()
            file_name = output["contents"][0]["name"]
            print(output)

            # Downloads the job output to a specified location on the hard drive.
            print("The file was converted and is being downloaded.")
            response = api_test.download_job_output(json_job["jobID"], "file")
            directory = os.path.join(file_out, file_name)
            __save_to_directory__(response, directory)
            name = filename.split('.')[0]
            uploaded_file_url = fs.url('pdf/' + name + '.docx')

            # Make sure to delete the job from the server once it is done.
            #print(api_test.delete_job(json_job["jobID"]))
            complete_url = 'https://journals.projecttopics.org' + uploaded_file_url #'http://localhost:8000' + uploaded_file_url
            return JsonResponse({'status':200, 'data':complete_url})
        except Exception as e:
            #print(api_test.delete_job(json_job["jobID"]))
            #raise e
            return JsonResponse({'status':400,'data': api_test.delete_job(json_job["jobID"]) })



def test(name_of_file):
    data = InputProperties.ImportProperties()
    data.load_properties()
    in_file = os.path.join(data.get_input_directory(), name_of_file)  # data.get_file_name())
    file_out = data.get_output_directory()
    usr_info = AppInfo.AppInfo(data.get_client_id(), data.get_client_secret())
    token_manager = TokenManager.TokenManager(TokenInfo.TokenInfo(""))
    try:
        api_test = EasyPDFCloud.EasyPDFCloudAPI(usr_info, token_manager)
    except KeyError:
        raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException("Unknown Parameter")

    # Creates a new job and uploads a file to convert.
    json_job = api_test.new_workflow_job(data.get_workflow_id(), in_file)
    print(json_job)
    try:
        # View info about the current job.
        print(api_test.get_job_info(json_job["jobID"]))

        # Wait for the job as it is being processed.
        while api_test.wait_for_job(json_job["jobID"]) is False:
            print("The job is currently running.")

        # Gives the output files name on the server.
        output = api_test.download_job_output(json_job["jobID"], "metadata").json()
        file_name = output["contents"][0]["name"]
        print(output)

        # Downloads the job output to a specified location on the hard drive.
        print("The file was converted and is being downloaded.")
        response = api_test.download_job_output(json_job["jobID"], "file")
        directory = os.path.join(file_out, file_name)
        __save_to_directory__(response, directory)

        # Make sure to delete the job from the server once it is done.
        print(api_test.delete_job(json_job["jobID"]))

    except Exception as e:
        print(api_test.delete_job(json_job["jobID"]))
        raise e






