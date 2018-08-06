from django.contrib import admin
from .models import Project, Wilaya, Specialite, Commune, Categorie


class JobAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_title', 'categorie',  'wilaya', 'commune', 'status', 'publish')
    list_filter = ('status', 'created', 'publish')
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

    prepopulated_fields = {'slug': ('project_title',)}

admin.site.register(Project, JobAdmin)
