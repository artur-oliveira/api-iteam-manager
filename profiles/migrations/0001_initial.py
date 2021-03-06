# Generated by Django 3.2.4 on 2021-06-20 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, max_length=1000)),
                ('url_hash', models.CharField(editable=False, max_length=15, unique=True)),
                ('secret_hash', models.CharField(editable=False, max_length=30, unique=True)),
                ('mostrar_perfil', models.BooleanField(default=True)),
                ('gratificado', models.IntegerField(default=0)),
                ('advertencias', models.IntegerField(default=0)),
                ('banido', models.IntegerField(default=0)),
                ('perfil_classifier', models.IntegerField(default=0)),
                ('interesses', models.ManyToManyField(blank=True, related_name='interesses', to='categories.Categoria')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
