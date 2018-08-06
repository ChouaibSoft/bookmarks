from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class Wilaya(models.Model):
    name = models.CharField(max_length=30)


    class Meta:
        ordering = ('name',)


    def __str__(self):
        return self.name


class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)



    def __str__(self):
        return self.name


class Categorie(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='category_image/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('name',)


    def __str__(self):
        return self.name


class Specialite(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)


    def __str__(self):
        return self.name



class Profile(models.Model):
    STATUS_CHOICES = (
        ('proprietaire', 'Proprietaire'),
        ('enteprise', 'Enteprise'),
    )
    type = models.CharField(max_length=12, choices=STATUS_CHOICES, default='proprietaire')
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=50)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    specialite = models.ManyToManyField(Specialite)
    overview = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True)
    facebook_url = models.URLField(max_length=200, blank=False)
    twitter_url = models.URLField(max_length=200, blank=False)
    youtube_url = models.URLField(max_length=200, blank=False)
    site_web = models.URLField(max_length=200, blank=False)
    phone = models.CharField(max_length=10, blank=True)
    phone1 = models.CharField(max_length=10)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='profiles_liked',
                                        blank=True)
    total_like = models.PositiveIntegerField(db_index=True, default=0)


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_absolute_url(self):
        return reverse('condidate_detail', args=[self.id, self.user.username])










