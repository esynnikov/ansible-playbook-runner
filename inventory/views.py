from django.shortcuts import render
from projects.dataaccess import getProjList
from .inventories import getInventoriesList, createInv, getInvProject,deleteInventory,editInventory,createInvStructure,getInv
from mainapp.main import uploadFiles,getProjName
import os

# Create your views here.

def inventory_init(request):
    currentproj = 'Project'
    currentprojid = 0
    projlist = getProjList()
    invlist = []
    currentinvid = 0
    if request.method == 'POST' and 'project' in request.POST:
        currentprojid = request.POST['project']
        currentproj = getProjName(currentprojid)
        invlist = getInventoriesList(currentprojid)
        return render (request,'pages/inventory/inv_main.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'invlist':invlist})
    elif request.method == 'POST' and 'inventory' in request.POST:
        currentinvid = request.POST['inventory']
        inv = getInv(currentinvid)
        currentprojid = inv.projectid
        currentproj = getProjName(currentprojid)
        invlist = getInventoriesList(currentprojid)
        return render (request,'pages/inventory/editinventory.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid,'invlist':invlist, 'inv': inv})
    elif request.method == 'POST' and 'GroupButton' in request.POST:
        currentinvid = request.POST['GroupButton']
        inv = getInv(currentinvid)
        currentprojid = inv.projectid
        currentproj = getProjName(currentprojid)
        invlist = getInventoriesList(currentprojid)
        files = request.FILES.getlist('GroupFile')
        path = '/opt/Projects/'+currentproj+'/inventories/'+inv.name+'/group_vars'
        uploadFiles(files,path)
        return render (request,'pages/inventory/editinventory.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid,'invlist':invlist, 'inv': inv})
    elif request.method == 'POST' and 'HostButton' in request.POST:
        currentinvid = request.POST['HostButton']
        inv = getInv(currentinvid)
        currentprojid = inv.projectid
        currentproj = getProjName(currentprojid)
        invlist = getInventoriesList(currentprojid)
        files = request.FILES.getlist('HostFile')
        path = '/opt/Projects/'+currentproj+'/inventories/'+inv.name+'/host_vars'
        uploadFiles(files,path)
        return render (request,'pages/inventory/editinventory.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid,'invlist':invlist, 'inv': inv})
    elif request.method == 'POST' and 'Upload' in request.POST:
        currentprojid = request.POST['Upload']
        currentproj = getProjName(currentprojid)
        description = request.POST['Description']
        name = request.POST['NameField']
        files = request.FILES.getlist('InputFile')
        filename = files[0].name
        basepath = '/opt/Projects/'+currentproj+'/inventories'
        createInvStructure(name,basepath)
        path = basepath+'/'+name
        uploadFiles(files,path)
        createInv(name,description,currentprojid,filename)
        invlist = getInventoriesList(currentprojid)
        return render (request,'pages/inventory/inv_main.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'invlist':invlist})
    elif request.method == 'POST' and 'Add' in request.POST:
        currentprojid = request.POST['Add']
        currentproj = getProjName(currentprojid)
        invlist = getInventoriesList(currentprojid)
        return render (request,'pages/inventory/loadinventory.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'invlist':invlist})
    elif request.method == 'POST' and 'Delete' in request.POST:
        currentinvid = request.POST['Delete']
        currentprojid = getInvProject(currentinvid)
        currentproj = getProjName(currentprojid)
        deleteInventory(currentinvid)
        invlist = getInventoriesList(currentprojid)
        return render (request,'pages/inventory/inv_main.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'invlist':invlist})
    elif request.method == 'POST' and 'Edit' in request.POST:
        currentinvid = request.POST['Edit']
        inv = getInv(currentinvid)
        currentprojid = inv.projectid
        currentproj = getProjName(currentprojid)
        path = '/opt/Projects/'+currentproj+'/inventories/'+inv.name+'/'+request.POST['InputFile']
        with open (path) as fl:
            filebody = fl.read()
        fl.close
        return render(request, 'pages/editfile.html',{'filebody':filebody,'path':path})
    elif request.method == 'POST' and 'Save' in request.POST:
        currentinvid = request.POST['Save']
        inv = getInv(currentinvid)
        currentprojid = inv.projectid
        currentproj = getProjName(currentprojid)
        editInventory(currentinvid,request.POST['Description'])
        invlist = getInventoriesList(currentprojid)
        return render (request,'pages/inventory/inv_main.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'invlist':invlist})
    elif request.method == 'POST' and 'SaveFile' in request.POST:
        with open(request.POST['Path'],'w') as fs:
            fs.write(request.POST['DescriptionField'])
        fs.close()
        return render(request, 'pages/successsave.html')
    else:
        return render (request,'pages/inventory/inv_main.html', {'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid})