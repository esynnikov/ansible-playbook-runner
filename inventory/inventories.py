from mainapp.models import inventories
from mainapp.main import makefolder, getProjName
import os
import shutil

def getInventoriesList(projectid):
    rows = inventories.objects.filter(projectid=projectid)
    return rows

def getInv(inventoryid):
    row = inventories.objects.get(id=inventoryid)
    return row

def getInvDescription(inventoryid):
    row = inventories.objects.get(id=inventoryid)
    return row.description

def getInvName(inventoryid):
    row = inventories.objects.get(id=inventoryid)
    return row.name

def getInvProject(inventoryid):
    row = inventories.objects.get(id=inventoryid)
    return row.projectid

def createInv(name,description,projectid,filename):
    row=inventories(name=name,description=description,projectid=projectid,filename=filename)
    row.save()

def deleteInventory(inventoryid):
    projectid = getInvProject(inventoryid)
    projectname = getProjName(projectid)
    row = inventories.objects.get(id=inventoryid)
    path = '/opt/Projects/'+projectname+'/inventories/'+row.name
    shutil.rmtree(path)
    row.delete()

def editInventory(inventoryid,description):
    row = inventories.objects.get(id=inventoryid)
    row.description = description
    row.save()

def createInvStructure(name,basepath):
    makefolder(basepath,name)
    makefolder(basepath+'/'+name,'group_vars')
    makefolder(basepath+'/'+name,'host_vars')



