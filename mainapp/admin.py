from django.contrib import admin
from .models import projects, playbooks, relations,inventories,buildset,buildsetitems,build,buildstep
# Register your models here.

admin.site.register(projects)
admin.site.register(playbooks)
admin.site.register(relations)
admin.site.register(inventories)
admin.site.register(buildset)
admin.site.register(buildsetitems)
admin.site.register(build)
admin.site.register(buildstep)
