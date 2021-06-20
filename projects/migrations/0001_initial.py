# Generated by Django 3.2.4 on 2021-06-20 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('url_hash', models.CharField(editable=False, max_length=10, unique=True)),
                ('share_hash', models.CharField(editable=False, max_length=20, unique=True)),
                ('descricao', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True, null=True)),
                ('privado', models.BooleanField(default=False)),
                ('encerrado', models.BooleanField(default=False)),
                ('administrador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='administrador', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioRecusado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualizou', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projeto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioGratificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualizou', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projeto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioConvidado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualizou', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projeto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioBanido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualizou', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projeto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioAdvertido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualizou', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projeto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioAceito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualizou', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projeto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='projeto',
            name='advertidos',
            field=models.ManyToManyField(blank=True, related_name='usuarios_advertidos', through='projects.UsuarioAdvertido', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='banidos',
            field=models.ManyToManyField(blank=True, related_name='usuarios_banidos', through='projects.UsuarioBanido', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='categoria',
            field=models.ManyToManyField(related_name='categorias_projeto', to='categories.Categoria'),
        ),
        migrations.AddField(
            model_name='projeto',
            name='convidados',
            field=models.ManyToManyField(blank=True, related_name='usuarios_convidados', through='projects.UsuarioConvidado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='criador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='gratificados',
            field=models.ManyToManyField(blank=True, related_name='usuarios_gratificados', through='projects.UsuarioGratificado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='moderador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moderador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='participantes',
            field=models.ManyToManyField(blank=True, related_name='participantes_projeto', through='projects.UsuarioAceito', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='pendentes',
            field=models.ManyToManyField(blank=True, related_name='usuarios_pendentes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='recusados',
            field=models.ManyToManyField(blank=True, related_name='usuarios_recusados', through='projects.UsuarioRecusado', to=settings.AUTH_USER_MODEL),
        ),
    ]