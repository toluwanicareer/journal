from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
import requests
import urllib
import xml.etree.ElementTree as ET
import pdb
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



# Create your views here.

class Home(TemplateView):
    template_name = 'index.html'


def clean_content(response):
    content = response.text
    index = content.find('<?xml')
    content = content[index:]
    return content

@method_decorator(csrf_exempt, name='dispatch')
class SearchJournal(View):

    def post(self, request, *args, **kwargs):
        search='http://www.journaltocs.ac.uk/api/journals/'
        query=request.POST.get('search')
        params={'user':'projecttopics@recode.ng'}
        search_url=search+query
        response=requests.get(search_url, params=urllib.parse.urlencode(params))
        try:
            content = clean_content(response)
            root=ET.fromstring(content)
        except KeyError:
            messages.warning(request, 'No record was found for "'+query+'"' )
            return HttpResponseRedirect('/')

        items=[]
        for item in root.findall('{http://purl.org/rss/1.0/}item'):
            item_dic = dict()
            item_dic['title']=item.find('{http://purl.org/rss/1.0/}title').text
            link=item.find('{http://purl.org/rss/1.0/}link').text
            description=item.find('{http://purl.org/rss/1.0/}description').text
            try:
                item_dic['issn']=item.find('{http'
                                           '://prismstandard.org/namespaces/1.2/basic/}issn').text
            except AttributeError:
                try:
                    item_dic['issn'] = item.find('{http://prismstandard.org/namespaces/1.2/basic/}eIssn').text
                except AttributeError:
                    messages.warning(request, 'No record was found for "' + query + '"')
                    return HttpResponseRedirect('/')
            publicationName=item.find('{http://prismstandard.org/namespaces/1.2/basic/}publicationName').text
            item_dic['publisher']=item.find('{http://purl.org/dc/elements/1.1/}publisher').text
            items.append(item_dic)
        #pdb.set_trace()
        return render(request, 'index.html', {'items':items, 'search_journal':True})

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')

class JournalDetail(View):

    def get(self,request, *args, **kwargs):
        issn=kwargs['issn']
        base_url='http://www.journaltocs.ac.uk/api/journals/'+issn
        params={'output':'articles', 'user':'projecttopics@recode.ng'}
        response=requests.get(base_url, params=urllib.parse.urlencode(params))
        #pdb.set_trace()
        content = clean_content(response)
        try:
            root=ET.fromstring(content)
        except ET.ParseError:
            content=content.replace('<name>', ',').replace('</name>', '')
            root=ET.fromstring(content)



        channel=root.find('{http://purl.org/rss/1.0/}channel')
        title=channel.find('{http://purl.org/rss/1.0/}title').text
        items = []
        for item in root.findall('{http://purl.org/rss/1.0/}item'):
            item_dic = dict()
            item_dic['title']=item.find('{http://purl.org/rss/1.0/}title').text
            item_dic['link']=item.find('{http://purl.org/rss/1.0/}link').text
            item_dic['description']=item.find('{http://purl.org/rss/1.0/}description').text
            item_dic['journal']=item.find('{http://prismstandard.org/namespaces/1.2/basic/}PublicationName').text
            try:
                item_dic['creator']=item.find('{http://purl.org/dc/elements/1.1/}creator').text
            except AttributeError:
                pass
            items.append(item_dic)
        return render(request, 'index.html', {'items':items, 'journal_page':True, 'journal_title':title.replace('JournalTOCs API -', '')})






def yandex(request):
    return render(request, 'yandex_e338a2b8290dc352.html')

def sitemap(request):
    return render(request, 'sitemap.xml')


def robot(request):
    return render(request, 'robots.txt')


