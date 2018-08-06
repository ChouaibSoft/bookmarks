from django.contrib import admin
from .models import Job, Wilaya, Specialite, Commune, Categorie


class JobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'categorie',  'wilaya', 'commune', 'status', 'publish')
    list_filter = ('status', 'created', 'publish')
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

    prepopulated_fields = {'slug': ('job_title',)}

admin.site.register(Job, JobAdmin)
