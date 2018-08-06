from django.contrib import admin
from .models import Profile, Wilaya, Commune, Categorie, Specialite


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'categorie', 'wilaya', 'commune']
    list_filter = ['user', 'wilaya', 'commune', 'categorie']


admin.site.register(Profile, ProfileAdmin)


class WilayaAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Wilaya, WilayaAdmin)


class CommuneAdmin(admin.ModelAdmin):
    list_display = ['name', 'wilaya']
    list_filter = ['wilaya']


admin.site.register(Commune, CommuneAdmin)


class CategorieAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Categorie, CategorieAdmin)


class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'categorie']
    list_filter = ['categorie']


admin.site.register(Specialite, SpecialiteAdmin)
