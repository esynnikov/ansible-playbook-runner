import os
import zipfile
import shutil
from os.path import isfile,join
from .models import projects

def uploadFiles(files,folderpath):
    for f in files:
            filename = f.name
            path = folderpath +'/' +filename
            with open (path,'wb+') as fl:
                for chunk in f.chunks():
                    fl.write(chunk)
            fl.close()

def unzipArchive(files,folderpath):
    for f in files:
            filename = f.name
            path = folderpath +'/' +filename
            zipref = zipfile.ZipFile(path,'r')
            zipref.extractall(folderpath)
            zipref.close
            os.remove(path)

def makefolder(basepath,name):
    fullpath = basepath+'/'+name
    if not os.path.exists(fullpath):
            os.makedirs(fullpath)

def getProjName(id):
    row = projects.objects.get(id=id)
    return row.name

def checkFile(path):
    if os.path.exists(path):
        res = True
    else:
        res = False
    return res

def clrFolder(path):
    for item in os.listdir(path):
        if isfile(join(path, item)):
            os.remove(join(path, item))
        else:
            shutil.rmtree(join(path, item))
        