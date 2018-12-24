import os.path
import AppInfo
import TokenInfo
import EasyPDFCloud
import TokenManager
import InputProperties
import EasyPDFCloudAPIExceptions


# Sample code to upload a file to the server, have it converted, and download the converted file to the computer.
def full_test(app_info, file_in, file_out, workflow_id):
    token_manager = TokenManager.TokenManager(TokenInfo.TokenInfo(""))
    try:
        api_test = EasyPDFCloud.EasyPDFCloudAPI(app_info, token_manager)
    except KeyError:
        raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException("Unknown Parameter")

    # Creates a new job and uploads a file to convert.
    json_job = api_test.new_workflow_job(workflow_id, file_in)
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


def __save_to_directory__(response, path):
    try:
        with open(path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except FileNotFoundError:
        print("No such file or directory: " + path)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Functions called below this line.
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

data = InputProperties.ImportProperties()
data.load_properties()
in_file = os.path.join(data.get_input_directory(), data.get_file_name())
usr_info = AppInfo.AppInfo(data.get_client_id(), data.get_client_secret())
full_test(usr_info, in_file, data.get_output_directory(), data.get_workflow_id())