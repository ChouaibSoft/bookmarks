from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import Categorie, Specialite, Wilaya, Commune
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings



class Project(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    PAYMENT_TYPE = (
        ('heure', 'par Heure'),
        ('semaine', 'par Semaine'),
        ('mois', 'par Mois'),
        ('projet', 'par Projet'),
        ('journee', 'par journée'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True, unique=False)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    specialite = models.ManyToManyField(Specialite)
    description = models.TextField(blank=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True)
    prix = models.PositiveIntegerField()
    phone = models.CharField(max_length=10, blank=True)
    phone1 = models.CharField(max_length=10)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    pay_type = models.CharField(max_length=15, choices=PAYMENT_TYPE, default='projet')
    users_follow = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='project_followed',
                                        blank=True)
    total_follow = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.project_title

    class Meta:
        ordering = ('-publish',)
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_title)
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project:project-detail', args=[self.id,
                                               self.slug])





