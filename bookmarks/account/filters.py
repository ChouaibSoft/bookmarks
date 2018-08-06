from django import forms
from .models import Profile, Commune, Specialite
import django_filters

class CondidateFilter(django_filters.FilterSet):
    profession = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['profession', 'wilaya', 'commune', 'categorie', 'specialite']

