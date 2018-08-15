from django.shortcuts import render
from projects.dataaccess import getProjList
from . import buildset
from tree.tree import printtree,getPlaybook,getplaybookid
from mainapp.models import bsitem
from mainapp.main import getProjName

# Create your views here.
def build_init(request):
    currentproj = 'Project'
    currentprojid = 0
    projlist = getProjList()
    if request.method == 'POST' and 'project' in request.POST:
        currentprojid=request.POST['project']
        currentproj=getProjName(currentprojid)
        #bslist = []
        bslist = buildset.getBsList(currentprojid)
        return render(request,'pages/buildset/bs_init.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist})
    elif request.method == 'POST' and 'Add' in request.POST:
        currentprojid = request.POST['Add']
        currentproj=getProjName(currentprojid)
        bslist = buildset.getBsList(currentprojid)
        lsttree = printtree(currentprojid)
        return render(request,'pages/buildset/buildsettools.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist, 'lsttree':lsttree})
    elif request.method == 'POST' and 'AddItemsNew' in request.POST:
        currentprojid = request.POST['AddItemsNew']
        currentproj=getProjName(currentprojid)
        bslist = buildset.getBsList(currentprojid)
        lsttree = printtree(currentprojid)
        lstplays = []
        i = 0
        for key in request.POST.keys():
            if key.find('playbook',0)!=-1:
                i=i+1
                for item in request.POST.getlist(key):
                    plid = getplaybookid(item,currentprojid)
               # es = key.find('_',9)
               # plid = key[9:es]
               # playbook = getPlaybook(plid)
                    bsi = bsitem(item,i,plid)
                    lstplays.append(bsi)
        for key in request.POST.keys():
            if key.find('tree',0)!=-1:
                playbooksid = request.POST.getlist(key)
                for id in playbooksid:
                    playbook = getPlaybook(id)
                    bsi = bsitem(playbook.path,i,id)
                    lstplays.append(bsi)
        
        return render(request,'pages/buildset/buildsettools.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist, 'lsttree':lsttree, 'lstplays': lstplays})
    elif request.method == 'POST' and 'AddItems' in request.POST:
        bsid = request.POST['AddItems']
        bs = buildset.getBs(bsid)
        currentprojid = bs.projectid
        currentproj=getProjName(currentprojid)
        bslist = buildset.getBsList(currentprojid)
        lsttree = printtree(currentprojid)
        i=0
        lstplays = []
        for key in request.POST.keys():
            if key.find('playbook',0)!=-1:
                i=i+1
                for item in request.POST.getlist(key):
                    plid = getplaybookid(item,currentprojid)
               # es = key.find('_',9)
               # plid = key[9:es]
               # playbook = getPlaybook(plid)
                    bsi = bsitem(item,i,plid)
                    lstplays.append(bsi)
        for key in request.POST.keys():
            if key.find('tree',0)!=-1:
                playbooksid = request.POST.getlist(key)
                for id in playbooksid:
                    playbook = getPlaybook(id)
                    bsi = bsitem(playbook.path,i,id)
                    lstplays.append(bsi)
        return render(request,'pages/buildset/buildsettools.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist, 'lsttree':lsttree, 'lstplays': lstplays, 'currentbs': bs})
    elif request.method == 'POST' and 'SaveNew' in request.POST:
        currentprojid = request.POST['SaveNew']
        currentproj=getProjName(currentprojid)
        bslist = buildset.getBsList(currentprojid)
        lsttree = printtree(currentprojid)
        currentbs = request.POST['NameField']
        bs = buildset.createBs(currentbs,request.POST['Description'],currentprojid)
        i = 0
        for key in request.POST.keys():
            if key.find('playbook',0)!=-1:
                i=i+1
                for item in request.POST.getlist(key):
                    plid = getplaybookid(item,currentprojid)
               # es = key.find('_',9)
               # plid = key[9:es]
               # playbook = getPlaybook(plid)
                #    bsi = bsitem(item,i,plid)
                #    lstplays.append(bsi)
                    buildset.createBsItem(bs.id,i,plid,currentprojid)
        lstplays = []
        for item in buildset.getBsItems(bs.id):
            i=i+1
            playbook = getPlaybook(item.playbookid)
            bsi = bsitem(playbook.path,i,item.playbookid)
            lstplays.append(bsi)
        return render(request,'pages/buildset/buildsettools.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist, 'lsttree':lsttree, 'lstplays': lstplays, 'currentbs': bs})
    elif request.method == 'POST' and 'Save' in request.POST:
        bsid =request.POST['Save']
        bs = buildset.getBs(bsid)
        bs.name = request.POST['NameField']
        bs.description = request.POST['Description']
        bs.save()
        currentprojid = bs.projectid
        currentproj=getProjName(currentprojid)
        bslist = buildset.getBsList(currentprojid)
        lsttree = printtree(currentprojid)
        i=0
        buildset.delBsItem(bsid)
        for key in request.POST.keys():
            if key.find('playbook',0)!=-1:
                i=i+1
                for item in request.POST.getlist(key):
                    plid = getplaybookid(item,currentprojid)
                    buildset.createBsItem(bsid,i,plid,currentprojid)
        lstplays = []
        i=0
        for item in buildset.getBsItems(bsid):
            i=i+1
            playbook = getPlaybook(item.playbookid)
            bsi = bsitem(playbook.path,i,item.playbookid)
            lstplays.append(bsi)
        return render(request,'pages/buildset/buildsettools.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist, 'lsttree':lsttree, 'lstplays': lstplays, 'currentbs': bs})
    elif request.method == 'POST' and 'bs' in request.POST:
        bsid = request.POST['bs']
        bs = buildset.getBs(bsid)
        currentprojid = bs.projectid
        currentproj=getProjName(currentprojid)
        
        bslist = buildset.getBsList(currentprojid)
        lsttree = printtree(currentprojid)
        lstplays = []
        i=0        
        for item in buildset.getBsItems(bsid):
            i=i+1
            playbook = getPlaybook(item.playbookid)
            bsi = bsitem(playbook.path,i,item.playbookid)
            lstplays.append(bsi)
        return render(request,'pages/buildset/buildsettools.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist, 'lsttree':lsttree, 'lstplays': lstplays, 'currentbs': bs})
    elif request.method == 'POST' and 'Delete' in request.POST:
        bsid = request.POST['Delete']
        bs = buildset.getBs(bsid)
        currentprojid = bs.projectid
        currentproj=getProjName(currentprojid)
        buildset.delBs(bsid)
        bslist = buildset.getBsList(currentprojid)
        return render(request,'pages/buildset/bs_init.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid,'bslist':bslist})
    else:
        return render(request,'pages/buildset/bs_init.html',{'projlist':projlist,'currentproj': currentproj, 'currentprojid': currentprojid})
