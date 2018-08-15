from mainapp.models import buildset,buildsetitems,playbooks,projects,buildsetitems

def getBsList(projectid):
    rows = buildset.objects.filter(projectid=projectid)
    return rows

def createBs(name,description,projectid):
    row = buildset(name=name,description=description,projectid=projectid)
    row.save()
    return row

def createBsItem(buildsetid,order,playbookid,projectid):
    row = buildsetitems(buildsetid=buildsetid,order=order,playbookid=playbookid,projectid=projectid)
    row.save()
    return row

def getBsItems(buildsetid):
    rows = buildsetitems.objects.filter(buildsetid=buildsetid).order_by('order')
    return rows

def delBsItem(buildsetid):
    buildsetitems.objects.filter(buildsetid=buildsetid).delete()

def delBs(buildsetid):
    buildsetitems.objects.filter(buildsetid=buildsetid).delete()
    buildset.objects.filter(id=buildsetid).delete()

def getBs(buildsetid):
    row = buildset.objects.get(id=buildsetid)
    return row

def getBsItem(id):
    row = buildsetitems.objects.get(id=id)
    return row

def getBsProj(buildsetid):
    row = buildset.objects.get(id=buildsetid)
    return row.projectid

def findBsItemByPlaybook(playbookid):
    rows = buildsetitems.objects.filter(playbookid=playbookid)
    return rows
