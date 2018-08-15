import os, json
from os import listdir
from os.path import isfile,join
from .models import playbooks, relations, pl


def addplaybook(fullpath, proj, ispar):
    row = playbooks(path=fullpath,projectid=proj,ischild=ispar)
    row.save()
    
def getplaybookid(fullpath, proj):
    row = playbooks.objects.get(path=fullpath,projectid=proj)
    return row.id

def addrelation(parid,childid):
    row = relations(parentid=parid, childid=childid)
    row.save()

def clrtable():
    relations.objects.all().delete()
    playbooks.objects.all().delete()
