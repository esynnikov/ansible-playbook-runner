from mainapp.ans import runplaybook
from tree.tree import getPlaybook
from buildset.buildset import getBsItems
from mainapp.models import build,buildstep
from mainapp.main import getProjName
import shutil
import os


def runBuild (inventory,buildset,project,bid,secret):
    inventorypath = '/opt/Projects/'+project+'/inventories/'+inventory.name+'/'+inventory.filename
    bstatus = 'Running'
    setStatus(bid,bstatus)
    for item in getBsItems(buildset.id):
            playbookpath = getPlaybook(item.playbookid).path
            setPlaybook(bid,item.playbookid)
            bstepid=createBuildStep(bid,playbookpath,'Running')
            result=runplaybook(inventorypath,playbookpath,project,getBuild(bid).name,secret)
            if result>0:
                bstatus = 'Failed'
                setItemStatus(bstepid,'Failed')
                break
            else:
                setItemStatus(bstepid,'Complete')
    if bstatus!='Failed':
        bstatus = 'Complete'
    setStatus(bid,bstatus)   
    setIdent(bid,0,'')


def createBuild(name,ident,procname,status,projectid):
    row=build(name=name,ident=ident,procname=procname,status=status,projectid=projectid)
    row.save()
    return row.id

def createBuildStep(buildid,path,status):
    row = buildstep(buildid=buildid,path=path,status=status)
    row.save()
    return row.id

def setIdent(id,ident,procname):
    row=build.objects.get(id=id)
    row.ident=ident
    row.procname=procname
    row.save()

def getBuild(id):
    row=build.objects.get(id=id)
    return row

def getBuildList(projectid):
    rows = build.objects.filter(projectid=projectid)
    return rows

def setPlaybook(id,playbook):
    row=build.objects.get(id=id)
    row.currentplay=playbook
    row.save()

def setStatus(id,status):
    row=build.objects.get(id=id)
    row.status=status
    row.save()

def setItemStatus(id,status):
    row=buildstep.objects.get(id=id)
    row.status=status
    row.save()

def delBuild(id):
    b=build.objects.get(id=id)
    projectname = getProjName(b.projectid)
    buildstep.objects.filter(buildid=id).delete()
    path = '/opt/Projects/'+projectname+'/logs/'+b.name+'out.log'
    os.remove(path)
    #path = '/opt/Projects/'+projectname+'/logs/'+b.name+'err.log'
    #os.remove(path)
    b.delete()

def getBuildStepList(bid):
    row = buildstep.objects.filter(buildid=bid)
    return row

def getBuildStep(id):
    row = buildstep.objects.get(id=id)
    return row