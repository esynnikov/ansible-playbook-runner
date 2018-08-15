from django.db import models

# Create your models here.
class projects(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

class playbooks(models.Model):
    path = models.TextField()
    projectid = models.IntegerField()
    ischild = models.BooleanField()

    def __str__(self):
        return self.path

class relations(models.Model):
    parentid = models.IntegerField()
    childid = models.IntegerField()
    projectid = models.IntegerField()

class inventories(models.Model):
    name = models.TextField()
    filename = models.TextField()
    description = models.TextField()
    projectid = models.IntegerField()

class buildset(models.Model):
    name = models.TextField()
    description = models.TextField()
    projectid = models.IntegerField()

class buildsetitems(models.Model):
    buildsetid = models.IntegerField()
    order = models.IntegerField()
    playbookid = models.IntegerField()
    projectid = models.IntegerField()

class build(models.Model):
    name = models.TextField()
    ident = models.IntegerField()
    procname = models.TextField()
    status = models.TextField()
    projectid = models.IntegerField()

class buildstep(models.Model):
    buildid = models.IntegerField()
    path = models.TextField()
    status = models.TextField()


class pl:
    def __init__(self,path,level,parent,id,available):
        self.path = path
        self.level = level
        self.parent = parent
        self.id = id
        self.available = available

class bsitem:
    def __init__(self,path,order,id):
        self.path = path
        self.order = order
        self.id=id
     
class bstep:
    def __init__(self,path,status):
        self.path = path
        self.status = status