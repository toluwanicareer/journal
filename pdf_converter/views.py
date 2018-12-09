from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import pdb
from .forms import UploadFileForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import File
# Create your views here.
from django.core.files.storage import FileSystemStorage
import convertapi
convertapi.api_secret = 'OzUJvmJf1jVlhO6Y'

@method_decorator(csrf_exempt, 'dispatch')
class ConvertView(View):

    def post(self, request, *args, **kwargs):
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        result=convertapi.convert('pdf', { 'File': 'https://journals.projecttopics.org/media/'+filename })
        name=filename.split('.')[0]
        result.file.save('media/pdf/'+name+'.pdf')
        uploaded_file_url = fs.url('pdf/'+name+'.pdf')
        complete_url='https://journals.projecttopics.org'+uploaded_file_url
        return JsonResponse({'file_url':complete_url})
