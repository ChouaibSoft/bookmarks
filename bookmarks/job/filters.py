from django import forms
from .models import Job, Commune, Specialite
import django_filters

class JobFilter(django_filters.FilterSet):
    job_title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ['job_title', 'wilaya', 'commune', 'categorie', 'specialite', 'prix', 'experience']

