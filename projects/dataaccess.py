from mainapp.models import projects, relations, playbooks,inventories,buildset
from buildset.buildset import getBsList,delBs
from inventory.inventories import getInventoriesList, deleteInventory
from mainapp.main import getProjName
from builds.build import delBuild,getBuildList
import os
import os.path
import shutil


def getProjList():
    projlist = projects.objects.all().order_by('name')
    return projlist

def getProjId(name):
    row = projects.objects.get(name=name)
    return row.id

def getProjDescription(id):
    row = projects.objects.get(id=id)
    return row.description

def saveProj(id,name,description):
    if id == '0':
        row=projects(name=name,description=description)
        row.save()
        path = '/opt/Projects/'+name
        if not os.path.exists(path):
            os.makedirs(path)
        invpath = path + '/inventories'
        if not os.path.exists(invpath):
            os.makedirs(invpath)
        respath = path + '/resources'
        if not os.path.exists(respath):
            os.makedirs(respath)
        plpath = path + '/playbooks'
        if not os.path.exists(plpath):
            os.makedirs(plpath)
        logpath = path + '/logs'
        if not os.path.exists(logpath):
            os.makedirs(logpath)
    else:
        row=projects.objects.get(id=id)
        row.name=name
        row.description=description
        row.save()
        return 0

def deleteProj(id):
    name = projects.objects.get(id=id).name
    for b in getBuildList(id):
        delBuild(b.id)
    for bs in getBsList(id):
        delBs(bs.id)
    for inv in getInventoriesList(id):
        deleteInventory(inv.id)
    relations.objects.filter(projectid=id).delete()
    playbooks.objects.filter(projectid=id).delete()
    projects.objects.filter(id=id).delete()
    path = '/opt/Projects/'+name
    shutil.rmtree(path)

def addproj():
    row=projects(name='test2',description='asds ad')
    row.save()

def getProject(id):
    row=projects.objects.get(id=id)
    return row