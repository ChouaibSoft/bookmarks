from django import forms
from .models import Project, Commune, Specialite
import django_filters

class JobFilter(django_filters.FilterSet):
    job_title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['project_title', 'wilaya', 'commune', 'categorie', 'specialite', 'prix', 'pay_type']

