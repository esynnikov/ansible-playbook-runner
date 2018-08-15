from django.shortcuts import render
from mainapp.models import projects
from .dataaccess import getProjList,saveProj,deleteProj,getProject

# Create your views here.
def projects_init(request):
    projlist = getProjList()
    projid = 0
    if request.method == "POST" and 'proj' in request.POST:
        projid=request.POST['proj']
        project = getProject(projid)
        return render(request, 'pages/projects/projecttools.html',{'projlist': projlist, 'projid':projid, 'projname':project.name,'description':project.description})
    elif request.method == "POST" and 'Add' in request.POST:
        projid = 0
        return render(request, 'pages/projects/projecttools.html',{'projlist': projlist, 'projid':projid})
    elif request.method == "POST" and 'Save' in request.POST:
                #query = '+'+request.POST['IdField']+'+'+' '+request.POST['NameField']+' '+request.POST['DescriptionField']
                saveProj(request.POST['IdField'],request.POST['NameField'],request.POST['DescriptionField'])
                return render(request, 'pages/projects/projects_main.html',{'projlist': projlist, 'projid':projid})
                #addproj()
    elif request.method == "POST" and 'Delete' in request.POST:
                deleteProj(request.POST['IdField'])
                return render(request, 'pages/projects/projects_main.html',{'projlist': projlist, 'projid':projid})
    else:
        return render(request, 'pages/projects/projects_main.html',{'projlist': projlist, 'projid':projid})