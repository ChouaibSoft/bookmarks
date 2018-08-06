from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import Categorie, Specialite, Wilaya, Commune
from django.urls import reverse


class Job(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True, unique=False)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    specialite = models.ManyToManyField(Specialite)
    description = models.TextField(blank=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True)
    prix = models.PositiveIntegerField()
    experience = models.PositiveIntegerField()
    phone = models.CharField(max_length=10, blank=True)
    phone1 = models.CharField(max_length=10)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ('-publish',)
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('job:job-detail', args=[self.id,
                                               self.slug])
