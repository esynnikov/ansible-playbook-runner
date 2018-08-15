from django.shortcuts import render
from projects.dataaccess import getProjList
from inventory.inventories import getInventoriesList, getInvName, getInvProject,getInv
from buildset.buildset import getBsList,getBs,getBsProj,getBsItems,getBsItem
from tree.tree import getPlaybook
from .build import runBuild, createBuild,setIdent,getBuild,getBuildList,delBuild,setStatus,getBuildStepList
from django.http import HttpResponseRedirect
from mainapp.models import bstep
from mainapp.main import getProjName
import threading
import datetime
# Create your views here.

def builds_init(request):
    currentproj = 'Project'
    currentprojid = 0
    projlist = getProjList()
    if request.method == 'POST' and 'project' in request.POST:
        currentprojid = request.POST['project'] 
        currentproj = getProjName(currentprojid)
        invlist = getInventoriesList(currentprojid)
        currentinv = ''
        currentbs = ''
        bslist = getBsList(currentprojid)
        buildlist=getBuildList(currentprojid)
        return render(request,'pages/builds/build_init.html',{'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'query':request.POST,'invlist':invlist, 'currentinv':currentinv,'bslist':bslist,'currentbs':currentbs, 'buildlist':buildlist, 'query':request.POST})
    elif request.method == 'POST' and 'inventory' in request.POST:
        currentinvid=request.POST['inventory']
        currentinv=getInv(currentinvid)
        currentprojid=getInvProject(currentinvid)
        currentproj = getProjName(currentprojid)
        invlist = getInventoriesList(currentprojid)
        currentbs = ''
        for key in request.POST.keys():
            if key.find('bstext_',0)!=-1:
                if len(key)>7:
                    bsid = key[7:]
                    currentbs = getBs(bsid)
        bslist = getBsList(currentprojid)
        buildlist=getBuildList(currentprojid)
        return render(request,'pages/builds/build_init.html',{'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'query':request.POST,'invlist':invlist, 'currentinv':currentinv,'bslist':bslist,'currentbs':currentbs, 'buildlist':buildlist,'query':request.POST})
    elif request.method == 'POST' and 'bs' in request.POST:
        bsid=request.POST['bs']
        currentbs=getBs(bsid)
        currentprojid=getBsProj(bsid)
        currentproj = getProjName(currentprojid)
        bslist = getBsList(currentprojid)
        invlist = getInventoriesList(currentprojid)
        currentinv = ''
        for key in request.POST.keys():
            if key.find('invtext_',0)!=-1:
                if len(key)>8:
                    invid = key[8:]
                    currentinv = getInv(invid)
        buildlist=getBuildList(currentprojid)
        return render(request,'pages/builds/build_init.html',{'projlist': projlist ,'currentproj':currentproj, 'currentprojid': currentprojid, 'query':request.POST,'invlist':invlist, 'currentinv':currentinv,'bslist':bslist,'currentbs':currentbs,'buildlist':buildlist, 'query':request.POST})
    elif request.method == 'POST' and 'Run' in request.POST:
        currentprojid=request.POST['Run']
        currentproj = getProjName(currentprojid)
        for key in request.POST.keys():
            if key.find('invtext_',0)!=-1:
                if len(key)>8:
                    invid = key[8:]
                    currentinv = getInv(invid)
        for key in request.POST.keys():
            if key.find('bstext_',0)!=-1:
                if len(key)>7:
                    bsid = key[7:]
                    currentbs = getBs(bsid)
        
        secret=request.POST['secret']
        runtime = datetime.datetime.now()
        bname = str(runtime.year)+str(runtime.month)+str(runtime.day)+str(runtime.hour)+str(runtime.minute)+str(runtime.second)
        ident = 0
        procname = ''
        status = 'Pending'

        bid = createBuild(bname,ident,procname,status,currentprojid)

        runthread = threading.Thread(target=runBuild,args=(currentinv,currentbs,currentproj,bid,secret))
        runthread.daemon=True
        runthread.start()
        #runthread.join()

        #if runthread.isAlive:
        setIdent(bid,runthread.ident,runthread.name)
        #proc = multiprocessing.Process(target=runBuild,args=(currentinv,currentbs,currentproj,bid,secret,))
        #proc.start()
        #setIdent(bid,proc.pid)
        
        projlist = getProjList()
        return render(request,'pages/builds/buildprocess.html',{'log': 'log', 'processid':bid,'status':status,'query':request.POST})  
    elif request.method == 'POST' and 'build' in request.POST:
        bid = request.POST['build']
        build = getBuild(bid)
        projectname=getProjName(build.projectid)
       # steps=[]
       # for item in getBuildStepList(bid):
       #     bsi = getBsItem(item.bsiid)
       #     path=getPlaybook(bsi.playbookid)
       #     step = bstep(path,item.status)
       #     steps.append(step)
        steps = getBuildStepList(bid)
        with open ('/opt/Projects/'+projectname+'/logs/'+build.name+'out.log','r') as fl:
            filebody = fl.read()
        fl.close()
        return render(request,'pages/builds/buildprocess.html',{'log': filebody, 'processid':bid,'status':build.status,'bitemlist':steps,'query':request.POST})  
    else:
        return render(request,'pages/builds/build_init.html',{'projlist': projlist, 'currentproj':currentproj, 'currentprojid': currentprojid, 'query':request.POST})
    
def logprocess(request):
   
    if request.method == 'GET' and 'Delete' in request.GET:
        buildid = request.GET['Delete']
        #projectname=getProjName(b.projectid)
        delBuild(buildid)
        return HttpResponseRedirect("/build/")
    else:
        buildid = request.GET['process']
        b = getBuild(buildid)
    
    thr = None
    thrname = 'None'
    if b.status!='Failed' and b.status!='Complete':
        thr = threading._active.get(b.ident)
        if thr is None:
            setIdent(buildid,0,'')
            setStatus(buildid,'Failed')
            thrname = 'None'
        else:
            if thr.name != b.procname:
                setIdent(buildid,0,'')
                setStatus(buildid,'Failed')
                thrname = thr.name
    projectname=getProjName(b.projectid)
    #steps=[]
    #for item in getBuildStepList(buildid):
    #    bsi = getBsItem(item.bsiid)
    #    path=getPlaybook(bsi.playbookid)
    #    step = bstep(path,item.status)
    #    steps.append(step)
    steps = getBuildStepList(buildid)
    with open ('/opt/Projects/'+projectname+'/logs/'+b.name+'out.log','r') as fl:
        filebody = fl.read()
    fl.close()

    return render(request,'pages/builds/buildprocess.html',{'log': filebody,'processid':buildid,'status':b.status,'bitemlist':steps,'query':thrname})  