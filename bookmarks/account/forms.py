from django import forms
from django.contrib.auth.models import User
from .models import Profile, Commune, Specialite



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('this mail is already used')
        return email


# Set Information for User ..
class UserEditForm(forms.ModelForm):
        first_name = forms.CharField(max_length=30,
                                     label='Prenom',
                                     required=False,
                                    widget=forms.TextInput
                                    (attrs={'placeholder': 'votre Prenom'}))
        last_name = forms.CharField(max_length=30,
                                    label='Nom',
                                    required=False,
                                widget=forms.TextInput
                                (attrs={'placeholder': 'votre Nom'}))

        class Meta:
            model = User
            fields = ('first_name', 'last_name')

class ProfileCreateForm(forms.ModelForm):

        name = forms.CharField(max_length=30,
                                     required=False,
                                     label='Nom de l\'enteprise',
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'ex campany.inc'}))



        overview = forms.CharField(max_length=500,
                                     label='À propos de toi',
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'Dérivez-vous..'}))

        experience = forms.CharField(max_length=500,
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'votre expérience dans votre domaine de travail'}))

        profession = forms.CharField(max_length=50,
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'ex. "Artisan"'}))

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

        facebook_url = forms.CharField(max_length=200,
                                       required=False,
                                       label='Facebook (optionel)',
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'inserer le lien'}))
        twitter_url = forms.CharField(max_length=200,
                                       required=False,
                                       label='Twitter (optionel)',
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'inserer le lien'}))
        youtube_url = forms.CharField(max_length=200,
                                       required=False,
                                       label='Youtube (optionel)',
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'inserer le lien'}))
        site_web = forms.CharField(max_length=200,
                                       required=False,
                                       label='Site Web (optionel)',
                                     widget=forms.TextInput
                                    (attrs={'placeholder': 'inserer le lien'}))

        class Meta:
            model = Profile
            fields = ['type', 'name', 'profession', 'categorie', 'specialite', 'overview', 'experience',
                      'date_of_birth', 'wilaya', 'commune', 'facebook_url',
                      'twitter_url', 'youtube_url', 'site_web', 'phone', 'phone', 'phone1', 'image']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['specialite'].queryset = Specialite.objects.none()

            if 'categorie' in self.data:
                try:
                    categorie_id = int(self.data.get('categorie'))
                    self.fields['specialite'].queryset = Specialite.objects.filter(
                        categorie_id=categorie_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty specialite queryset
            elif self.instance.pk:
                self.fields['specialite'].queryset = self.instance.categorie.specialite_set.order_by('name')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['specialite'].queryset = Specialite.objects.none()

            if 'categorie' in self.data:
                try:
                    categorie_id = int(self.data.get('categorie'))
                    self.fields['specialite'].queryset = Specialite.objects.filter(
                        categorie_id=categorie_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty specialite queryset
            elif self.instance.pk:
                self.fields['specialite'].queryset = self.instance.categorie.specialite_set.order_by('name')



        def save(self, force_insert=False, force_update=False, commit=True):
            profile = super(ProfileCreateForm, self).save(commit=False)

            if commit:
                profile.save()
            return profile



