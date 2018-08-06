from django import forms

from .models import Job


class JobCreateForm(forms.ModelForm):

    job_title = forms.CharField(max_length=250,
                           label='Titre',
                           widget=forms.TextInput
                           (attrs={'placeholder': 'titre'}))


    phone = forms.CharField(max_length=10,
                            label='Numero Telephone',
                            required=True,
                            widget=forms.TextInput
                            (attrs={'placeholder': 'votre numero Telephone 1"'}))

    phone1 = forms.CharField(max_length=10,
                             required=False,
                             label='Numero Telephone 2 (optionel)',
                             widget=forms.TextInput
                             (attrs={'placeholder': 'votre numero Telephone 2"'}))



    class Meta:
        model = Job
        fields = ['job_title', 'categorie', 'specialite', 'description', 'prix',
                  'experience', 'wilaya', 'commune', 'phone', 'phone1']
