import os, json
import yaml
from os import listdir
from os.path import isfile,join
from mainapp.models import playbooks, relations, pl
from buildset.buildset import findBsItemByPlaybook,delBs
from mainapp.main import checkFile

def crttree(projfolder, projectid):
    exclude = set(['inventories','resources'])
    for path, subdirs, files in os.walk(projfolder):
        subdirs[:] = [d for d in subdirs if d not in exclude]
        for item in files:
            if isfile(join(path, item)):
                yamlf = item.find('.yaml',0)
                ymlf = item.find('.yml',0)
                if yamlf==len(item)-5 or ymlf==len(item)-4:
                    with open (join(path, item),'r',encoding='utf-8') as stream:
                        try:
                            data=yaml.load(stream)
                            if data is not None:
                                for key in data:
                                    if 'hosts' or 'import_playbook' in key:
                                        fnd = playbooks.objects.filter(projectid=projectid,path=join(path,item)).count()
                                        if fnd == 0:
                                            addplaybook (join(path,item),projectid,False)
                                        findbind (path,item,projectid)
                                        break
                        except yaml.YAMLError:
                            pass
                
                #    fnd = playbooks.objects.filter(projectid=projectid,path=join(path,item)).count()
                #    if fnd == 0:
                #        addplaybook (join(path,item),projectid,False)
                #    findbind (path,item,projectid)

def findbind(path, filename,projectid):
    parentid = getplaybookid(join(path,filename),projectid)
    with open (join(path,filename),'r') as fl:
        for line in fl:
            dstring = line.rstrip('\n')
            ipstr = dstring.find('import_playbook',0)
            if ipstr != -1:
                commstr = dstring.find('#',ipstr)
                if commstr != -1:
                    bindname = dstring[ipstr+17:commstr].strip(" ")
                else:   
                    bindname = dstring[ipstr+17:].strip(" ")

                fnd = playbooks.objects.filter(projectid=projectid,path=join(path,bindname)).count()
                if fnd != 0:
                    row = playbooks.objects.get(path=join(path,bindname),projectid=projectid)
                    row.ischild = True
                    childid = row.id
                    row.save()
                else:
                    addplaybook(join(path,bindname),projectid,True)
                    childid=getplaybookid(join(path,bindname),projectid)
                addrelation(parentid,childid,projectid)

def addplaybook(fullpath, proj, ispar):
    row = playbooks(path=fullpath,projectid=proj,ischild=ispar)
    row.save()
    
def getplaybookid(fullpath, proj):
    row = playbooks.objects.get(path=fullpath,projectid=proj)
    return row.id

def getPlaybook(playbookid):
    row = playbooks.objects.get(id=playbookid)
    return row

def addrelation(parid,childid,projectid):
    row = relations(parentid=parid, childid=childid, projectid=projectid)
    row.save()

def clrtree(projectid):
    for playbook in playbooks.objects.filter(projectid=projectid):
        for bsi in findBsItemByPlaybook(playbook.id):
            delBs(bsi.buildsetid)
    relations.objects.filter(projectid=projectid).delete()
    playbooks.objects.filter(projectid=projectid).delete()


def printtree(proj):
    parents = playbooks.objects.filter(projectid=proj,ischild=False).order_by('id')
    lst = []
    
    def addchilds (parentlist, level, upperlevel):
        for row in parentlist:
            if level == 0:
                margin = 1
            elif level > 10:
                break
            else:
                margin = level+1
            tmp = pl(row.path,margin,upperlevel,row.id,checkFile(row.path))
            lst.append(tmp)
            childs = relations.objects.filter(parentid=row.id).order_by('id')
            for rowchild in childs:
                child = playbooks.objects.filter(projectid=proj,id=rowchild.childid)
                #lst.append(('-'*(level+1))+child.path)
                addchilds(child,level+1,row.id)
  
    addchilds(parents,0,0)
    return lst

def getPlaybooksCountByProjId(projectid):
    cnt = playbooks.objects.filter(projectid=projectid).count()
    return cnt

def delPlFromTree(playbookid):
    playbooks.objects.get(id=playbookid).delete()

def getProjFromPlId(playbookid):
    row = playbooks.objects.get(id=playbookid)
    for bsi in findBsItemByPlaybook(playbookid):
            delBs(bsi.buildsetid)
    return row.projectid