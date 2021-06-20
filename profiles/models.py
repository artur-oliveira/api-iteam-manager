import random
import string
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from categories.models import Categoria


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    descricao = models.TextField(max_length=1000, blank=True)
    interesses = models.ManyToManyField(Categoria, related_name='interesses', blank=True)
    url_hash = models.CharField(max_length=15, unique=True, editable=False)
    secret_hash = models.CharField(max_length=30, unique=True, editable=False)
    mostrar_perfil = models.BooleanField(default=True)

    gratificado = models.IntegerField(default=0)
    advertencias = models.IntegerField(default=0)
    banido = models.IntegerField(default=0)
    perfil_classifier = models.IntegerField(default=0)

    @staticmethod
    def id_generator(size=15, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.url_hash == '' or self.url_hash is None:
            self.url_hash = self.id_generator(size=15)
            while Profile.objects.filter(url_hash=self.url_hash).exists():
                self.url_hash = self.id_generator(size=15)

        if self.secret_hash == '' or self.secret_hash is None:
            self.secret_hash = self.id_generator(size=30)
            while Profile.objects.filter(secret_hash=self.secret_hash).exists():
                self.secret_hash = self.id_generator(size=30)

        self.perfil_classifier = (4 * self.gratificado) - self.advertencias - (3 * self.banido)
        super(Profile, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '%s - profile' % self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
