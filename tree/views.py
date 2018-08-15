from django.shortcuts import render
from projects.views import getProjList
from django.http import HttpResponse
from .tree import getPlaybooksCountByProjId,crttree,printtree,clrtree,delPlFromTree,getProjFromPlId
from mainapp.main import uploadFiles, unzipArchive, getProjName,clrFolder

# Create your views here.

def tree_init(request):
    projlist = getProjList()
    currentproj = 'Project'
    currentprojid = 0
    lsttree = []
    if request.method == 'POST' and 'project' in request.POST:
        currentproj = getProjName(request.POST['project'])
        currentprojid = request.POST['project']
        cnt = getPlaybooksCountByProjId(request.POST['project'])
        if cnt == 0:
            return render(request, 'pages/tree/empty_proj.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid ,'lsttree':lsttree})
        else:
            lsttree=printtree(request.POST['project'])
        return render(request, 'pages/tree/tree_main.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid ,'lsttree':lsttree})
    elif request.method == 'POST' and 'DownloadButton' in request.POST:
         with open (request.POST['DownloadButton'],'r') as fl:
            response = HttpResponse(fl.read(), content_type="text/plain")
            return response
         fl.close()
    elif request.method == 'POST' and 'EditButton' in request.POST:
        with open (request.POST['EditButton']) as fl:
            filebody = fl.read()
        fl.close
        return render(request, 'pages/editfile.html',{'filebody':filebody,'path':request.POST['EditButton']})
    elif request.method == 'POST' and 'SaveFile' in request.POST:
        with open(request.POST['Path'],'w') as fs:
            fs.write(request.POST['DescriptionField'])
        fs.close()
        return render(request, 'pages/successsave.html')
    elif request.method == 'POST' and 'ReCreate' in request.POST:
        currentprojid = request.POST['ReCreate']
        currentproj = getProjName(currentprojid)
        path = '/opt/Projects/'+currentproj+'/playbooks'
        clrtree(currentprojid)
        crttree(path,currentprojid)
        lsttree=printtree(currentprojid)
        return render(request, 'pages/tree/tree_main.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid,'lsttree':lsttree})
    elif request.method == 'POST' and 'Clear' in request.POST:
        currentprojid = request.POST['Clear']
        currentproj = getProjName(currentprojid)
        path = '/opt/Projects/'+currentproj+'/playbooks'
        clrtree(currentprojid)
        clrFolder(path)
        return render(request, 'pages/tree/tree_main.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid})
    elif request.method == 'POST' and 'DelButton' in request.POST:
        plid = request.POST['DelButton']
        currentprojid=getProjFromPlId(plid)
        currentproj = getProjName(currentprojid)
        delPlFromTree(plid)
        lsttree=printtree(currentprojid)
        return render(request, 'pages/tree/tree_main.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid,'lsttree':lsttree})
    elif request.method == 'POST' and 'FileButton' in request.POST:
        currentprojid = request.POST['FileButton']
        currentproj = getProjName(currentprojid)
        files = request.FILES.getlist('InputFile')
        path = path = '/opt/Projects/'+currentproj+'/playbooks'
        uploadFiles(files,path)
        clrtree(currentprojid)
        crttree(path,currentprojid)
        lsttree=printtree(currentprojid)
        return render(request, 'pages/tree/tree_main.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid,'lsttree':lsttree})
    elif request.method == 'POST' and 'ZipButton' in request.POST:
        currentprojid = request.POST['ZipButton']
        currentproj = getProjName(currentprojid)
        files = request.FILES.getlist('InputZip')
        path = path = '/opt/Projects/'+currentproj+'/playbooks'
        uploadFiles(files,path)
        unzipArchive(files,path)
        clrtree(currentprojid)
        crttree(path,currentprojid)
        lsttree=printtree(currentprojid)
        return render(request, 'pages/tree/tree_main.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid,'lsttree':lsttree})
    else:
        return render(request, 'pages/tree/tree_main.html',{'projlist':projlist, 'currentproj':currentproj, 'currentprojid': currentprojid, 'lsttree':lsttree})
    
