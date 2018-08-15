from .tst_python import glist
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext



# Create your views here.
def index(request):
    return render (request, 'pages/home.html')


def downloadFile(path):
    with open (path,'r') as fl:
        response = HttpResponse(fl.read(), content_type="text/plain")
        return response

def browseFile(request):
    return render (request, 'pages/browse.html', {'pst2': request.POST,'query':'query'})