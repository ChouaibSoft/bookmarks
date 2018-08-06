# Generated by Django 2.0 on 2018-06-10 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(db_index=True, max_length=250)),
                ('slug', models.SlugField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('prix', models.PositiveIntegerField()),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('phone1', models.CharField(max_length=10)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('pay_type', models.CharField(choices=[('heure', 'par Heure'), ('semaine', 'par Semaine'), ('mois', 'par Mois'), ('projet', 'par Projet'), ('journee', 'par journée')], default='projet', max_length=15)),
                ('total_follow', models.PositiveIntegerField(db_index=True, default=0)),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Categorie')),
                ('commune', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Commune')),
                ('specialite', models.ManyToManyField(to='account.Specialite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('users_follow', models.ManyToManyField(blank=True, related_name='project_followed', to=settings.AUTH_USER_MODEL)),
                ('wilaya', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Wilaya')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.AlterIndexTogether(
            name='project',
            index_together={('id', 'slug')},
        ),
    ]