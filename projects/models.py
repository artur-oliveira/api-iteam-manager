import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from categories.models import Categoria


class UsuarioRecusado(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizou = models.BooleanField(default=False)

    @staticmethod
    def salvar(projeto, user, visualizou=False):
        try:
            u = UsuarioRecusado.objects.get(projeto=projeto, user=user)
            u.visualizou = visualizou
            u.save()
            return u

        except UsuarioRecusado.DoesNotExist:
            u = UsuarioRecusado(projeto=projeto, user=user, visualizou=visualizou)
            u.save()
            return u

    def __str__(self):
        return '%s recusado %s' % (self.user.first_name, self.projeto.nome)

    def __repr__(self):
        return self.__str__()


class UsuarioAceito(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizou = models.BooleanField(default=False)

    @staticmethod
    def salvar(projeto, user, visualizou=False):
        try:
            u = UsuarioAceito.objects.get(projeto=projeto, user=user)
            u.visualizou = visualizou
            u.save()
            return u

        except UsuarioAceito.DoesNotExist:
            u = UsuarioAceito(projeto=projeto, user=user, visualizou=visualizou)
            u.save()
            return u

    def __str__(self):
        return '%s aceito %s' % (self.user.first_name, self.projeto.nome)

    def __repr__(self):
        return self.__str__()


class UsuarioBanido(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizou = models.BooleanField(default=False)

    @staticmethod
    def salvar(projeto, user, visualizou=False):
        try:
            u = UsuarioBanido.objects.get(projeto=projeto, user=user)
            u.visualizou = visualizou
            u.save()
            return u

        except UsuarioBanido.DoesNotExist:
            u = UsuarioBanido(projeto=projeto, user=user, visualizou=visualizou)
            u.save()
            return u

    def __str__(self):
        return '%s banido %s' % (self.user.first_name, self.projeto.nome)

    def __repr__(self):
        return self.__str__()


class UsuarioAdvertido(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizou = models.BooleanField(default=False)

    @staticmethod
    def salvar(projeto, user, visualizou=False):
        try:
            u = UsuarioAdvertido.objects.get(projeto=projeto, user=user)
            u.visualizou = visualizou
            u.save()
            return u

        except UsuarioAdvertido.DoesNotExist:
            u = UsuarioAdvertido(projeto=projeto, user=user, visualizou=visualizou)
            u.save()
            return u

    def __str__(self):
        return '%s advertido %s' % (self.user.first_name, self.projeto.nome)

    def __repr__(self):
        return self.__str__()


class UsuarioGratificado(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizou = models.BooleanField(default=False)

    @staticmethod
    def salvar(projeto, user, visualizou=False):
        try:
            u = UsuarioGratificado.objects.get(projeto=projeto, user=user)
            u.visualizou = visualizou
            u.save()
            return u

        except UsuarioGratificado.DoesNotExist:
            u = UsuarioGratificado(projeto=projeto, user=user, visualizou=visualizou)
            u.save()
            return u

    def __str__(self):
        return '%s gratificado %s' % (self.user.first_name, self.projeto.nome)

    def __repr__(self):
        return self.__str__()


class UsuarioConvidado(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizou = models.BooleanField(default=False)

    @staticmethod
    def salvar(projeto, user, visualizou=False):
        try:
            u = UsuarioConvidado.objects.get(projeto=projeto, user=user)
            u.visualizou = visualizou
            u.save()
            return u

        except UsuarioConvidado.DoesNotExist:
            u = UsuarioConvidado(projeto=projeto, user=user, visualizou=visualizou)
            u.save()
            return u

    def __str__(self):
        return '%s convidado %s' % (self.user.first_name, self.projeto.nome)

    def __repr__(self):
        return self.__str__()


class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    url_hash = models.CharField(max_length=10, unique=True, editable=False)
    share_hash = models.CharField(max_length=20, unique=True, editable=False)
    descricao = models.TextField()

    criador = models.ForeignKey(User, related_name='criador', on_delete=models.CASCADE)
    administrador = models.ForeignKey(User, related_name='administrador', on_delete=models.SET_NULL, null=True,
                                      blank=True)
    moderador = models.ForeignKey(User, related_name='moderador', on_delete=models.SET_NULL, null=True, blank=True)

    participantes = models.ManyToManyField(User, related_name='participantes_projeto', blank=True,
                                           through=UsuarioAceito)
    pendentes = models.ManyToManyField(User, related_name='usuarios_pendentes', blank=True)
    recusados = models.ManyToManyField(User, related_name='usuarios_recusados', blank=True,
                                       through=UsuarioRecusado)
    convidados = models.ManyToManyField(User, related_name='usuarios_convidados', blank=True, through=UsuarioConvidado)
    banidos = models.ManyToManyField(User, related_name='usuarios_banidos', blank=True, through=UsuarioBanido)

    advertidos = models.ManyToManyField(User, related_name='usuarios_advertidos', blank=True,
                                        through=UsuarioAdvertido)
    gratificados = models.ManyToManyField(User, related_name='usuarios_gratificados', blank=True,
                                          through=UsuarioGratificado)

    categoria = models.ManyToManyField(Categoria, related_name='categorias_projeto')
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    privado = models.BooleanField(default=False)
    encerrado = models.BooleanField(default=False)

    @staticmethod
    def projetos_com_acesso(user):
        return Projeto.objects.filter(Q(criador=user) | Q(administrador=user))

    @staticmethod
    def projetos_que_participa(user):
        return Projeto.objects.filter(Q(criador=user) | Q(participantes=user)).order_by('-data_criacao').distinct()

    @staticmethod
    def projetos_para_explorar(user):
        participando = [int(a.get('projeto')) for a in UsuarioAceito.objects.filter(user=user).values('projeto')]
        banido = [int(a.get('projeto')) for a in UsuarioBanido.objects.filter(user=user).values('projeto')]
        recusado = [int(a.get('projeto')) for a in UsuarioRecusado.objects.filter(user=user).values('projeto')]

        return Projeto.objects.filter(privado=False, encerrado=False).\
            exclude(id__in=participando).exclude(id__in=banido).exclude(id__in=recusado)

    @staticmethod
    def id_generator(size=10, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.url_hash == '' or self.url_hash is None:
            self.url_hash = self.id_generator(size=10)
            while Projeto.objects.filter(url_hash=self.url_hash).exists():
                self.url_hash = self.id_generator(size=10)
        if self.share_hash == '' or self.share_hash is None:
            self.share_hash = self.id_generator(size=20)
            while Projeto.objects.filter(share_hash=self.share_hash).exists():
                self.share_hash = self.id_generator(size=20)

        super(Projeto, self).save(force_insert, force_update, using, update_fields)

    def has_access(self, user: User):
        return self.criador_id == user.id or self.administrador_id == user.id

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()
