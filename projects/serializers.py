from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Projeto, UsuarioAceito, UsuarioConvidado, UsuarioRecusado, UsuarioConviteRecusado


class ProjetoSerializer(serializers.ModelSerializer):
    invite_url = serializers.SerializerMethodField()

    class Meta:
        model = Projeto
        fields = ('nome', 'descricao', 'categoria', 'invite_url',)
        write_only_fields = ('nome', 'descricao', 'categoria', 'privado')
        read_only_fields = ('criador', )

    @staticmethod
    def get_invite_url(instance):
        return instance.url_hash

    def create(self, validated_data):
        current_user: User = self.context.get('request').user
        p = Projeto()
        p.nome = validated_data.get('nome', None)
        p.descricao = validated_data.get('descricao', None)
        p.privado = validated_data.get('privado', False)
        p.criador = current_user
        p.save()

        p.categoria.set(validated_data.get('categoria', None))
        UsuarioAceito.objects.create(projeto=p, user=current_user, visualizou=True)

        return p


class RequestParticipationSerializer(serializers.Serializer):
    class Meta:
        fields = ('success', )
        write_only_fields = ('invite_url', )

    invite_url = serializers.CharField(max_length=15, required=True)
    success = serializers.CharField(max_length=500, required=False)
    error = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):
        attrs = super(RequestParticipationSerializer, self).validate(attrs)
        try:
            current_user: User = self.context.get('request').user
            p = Projeto.objects.get(url_hash=attrs.get('invite_url'))

            if current_user in p.participantes.all():
                raise ValidationError(detail={'error': 'Você já está neste projeto'})
        except Projeto.DoesNotExist:
            raise ValidationError(detail={'error': 'Este projeto não existe'})

        return attrs

    def create(self, validated_data):
        current_user: User = self.context.get('request').user
        p = Projeto.objects.get(url_hash=validated_data.get('invite_url'))
        p.pendentes.add(current_user)
        p.save()

        return {
            'success': 'Solicitação enviada com sucesso',
            'invite_url': validated_data.get('invite_url')
        }

    def update(self, instance, validated_data):
        return instance


class AcceptParticipationSerializer(serializers.Serializer):
    class Meta:
        fields = ('success',)
        write_only_field = ('project', 'user', )

    project = serializers.IntegerField()
    user = serializers.IntegerField()

    success = serializers.CharField(max_length=500, required=False)
    error = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):
        attrs = super(AcceptParticipationSerializer, self).validate(attrs)
        try:
            current_user: User = self.context.get('request').user
            request_user = attrs.get('user')
            p = Projeto.objects.get(id=attrs.get('project'))
            user = User.objects.get(id=request_user)

            if not p.has_access(current_user):
                raise ValidationError(detail={'error': 'Você não tem acesso a este projeto'})

            pendentes = [u.id for u in p.pendentes.all()]
            banidos = [u.id for u in p.banidos.all()]
            recusados = [u.id for u in p.recusados.all()]

            if user.id not in pendentes:
                raise ValidationError(detail={'error': 'Este usuário não solicitou a participação neste projeto'})

            if user.id in banidos or user.id in recusados:
                raise ValidationError(detail={'error': 'Este usuário não pode realizar solicitações neste projeto'})

        except Projeto.DoesNotExist:
            raise ValidationError(detail={'error': 'Este projeto não existe'})
        except User.DoesNotExist:
            raise ValidationError(detail={'error': 'Este usuário não existe'})

        return attrs

    def create(self, validated_data):
        p = Projeto.objects.get(id=validated_data.get('project'))
        user = User.objects.get(id=validated_data.get('user'))

        UsuarioAceito.objects.create(projeto=p, user=user, visualizou=False)
        p.pendentes.remove(user)
        p.save()

        return {
            'success': 'Usuário aceito com sucesso',
            'project': validated_data.get('project'),
            'user': validated_data.get('user')
        }

    def update(self, instance, validated_data):
        return instance


class DenyParticipationSerializer(serializers.Serializer):
    class Meta:
        fields = ('success',)
        write_only_field = ('project', 'user',)

    project = serializers.IntegerField()
    user = serializers.IntegerField()

    success = serializers.CharField(max_length=500, required=False)
    error = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):
        attrs = super(DenyParticipationSerializer, self).validate(attrs)
        try:
            current_user: User = self.context.get('request').user
            request_user = attrs.get('user')
            p = Projeto.objects.get(id=attrs.get('project'))
            user = User.objects.get(id=request_user)

            if not p.has_access(current_user):
                raise ValidationError(detail={'error': 'Você não tem acesso a este projeto'})

            pendentes = [u.id for u in p.pendentes.all()]
            banidos = [u.id for u in p.banidos.all()]
            recusados = [u.id for u in p.recusados.all()]

            if user.id not in pendentes:
                raise ValidationError(detail={'error': 'Este usuário não solicitou a participação neste projeto'})

            if user.id in banidos or user.id in recusados:
                raise ValidationError(detail={'error': 'Este usuário não pode realizar solicitações neste projeto'})

        except Projeto.DoesNotExist:
            raise ValidationError(detail={'error': 'Este projeto não existe'})
        except User.DoesNotExist:
            raise ValidationError(detail={'error': 'Este usuário não existe'})

        return attrs

    def create(self, validated_data):
        p = Projeto.objects.get(id=validated_data.get('project'))
        user = User.objects.get(id=validated_data.get('user'))

        UsuarioRecusado.objects.create(projeto=p, user=user, visualizou=False)
        p.pendentes.remove(user)
        p.save()

        return {
            'success': 'Usuário recusado com sucesso',
            'project': validated_data.get('project'),
            'user': validated_data.get('user')
        }

    def update(self, instance, validated_data):
        return instance


class RequestInviteSerializer(serializers.Serializer):
    class Meta:
        fields = ('success',)
        write_only_field = ('project', 'user',)

    project = serializers.IntegerField()
    user = serializers.IntegerField()

    success = serializers.CharField(max_length=500, required=False)
    error = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):
        attrs = super(RequestInviteSerializer, self).validate(attrs)
        try:
            current_user: User = self.context.get('request').user

            request_user = attrs.get('user')
            p = Projeto.objects.get(id=attrs.get('project'))
            if not p.has_access(current_user):
                raise ValidationError(detail={'error': 'Você não tem acesso a este projeto'})

            user = User.objects.get(id=request_user)

            pendentes = [u.id for u in p.pendentes.all()]
            banidos = [u.id for u in p.banidos.all()]
            recusados = [u.id for u in p.recusados.all()]
            convites_recusados = [u.id for u in p.convites_recusados.all()]

            if user.id in pendentes:
                raise ValidationError(detail={'error': 'Este usuário já solicitou um convite, aceite-o para que ele '
                                                       'possa colaborar no projeto'})

            if user.id in convites_recusados:
                raise ValidationError(detail={'error': 'Este usuário recusou o convite. Não é possível convidá-lo, '
                                                       'se você o conhece, compartilhe a chave do projeto para que '
                                                       'ele possa colaborar'})

            if user.id in recusados:
                raise ValidationError(detail={'error': 'Este usuário foi recusado. Compartilhe a '
                                                       'chave do projeto para que ele possa entrar no projeto'})

            if user.id in banidos:
                raise ValidationError(detail={'error': 'Este usuário foi banido. Compartilhe a '
                                                       'chave do projeto para que ele possa entrar no projeto'})

        except Projeto.DoesNotExist:
            raise ValidationError(detail={'error': 'Este projeto não existe'})
        except User.DoesNotExist:
            raise ValidationError(detail={'error': 'Este usuário não existe'})

        return attrs

    def create(self, validated_data):
        p = Projeto.objects.get(id=validated_data.get('project'))
        user = User.objects.get(id=validated_data.get('user'))

        UsuarioConvidado.objects.create(projeto=p, user=user, visualizou=False)

        return {
            'success': 'Usuário convidado com sucesso',
            'project': validated_data.get('project'),
            'user': validated_data.get('user')
        }

    def update(self, instance, validated_data):
        return instance


class AcceptInviteSerializer(serializers.Serializer):
    class Meta:
        fields = ('success',)
        write_only_field = ('project', 'user',)

    project = serializers.IntegerField()
    user = serializers.IntegerField()

    success = serializers.CharField(max_length=500, required=False)
    error = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):
        attrs = super(AcceptInviteSerializer, self).validate(attrs)
        try:
            user: User = self.context.get('request').user
            p = Projeto.objects.get(id=attrs.get('project'))

            convidados = [u.id for u in p.convidados.all()]
            banidos = [u.id for u in p.banidos.all()]
            recusados = [u.id for u in p.recusados.all()]

            if user.id not in convidados:
                raise ValidationError(detail={'error': 'Você não foi convidado para este projeto'})

            if user.id in banidos or user.id in recusados:
                raise ValidationError(detail={'error': 'Você não pode aceitar solicitações neste projeto'})

        except Projeto.DoesNotExist:
            raise ValidationError(detail={'error': 'Este projeto não existe'})
        except User.DoesNotExist:
            raise ValidationError(detail={'error': 'Este usuário não existe'})

        return attrs

    def create(self, validated_data):
        p = Projeto.objects.get(id=validated_data.get('project'))
        user = User.objects.get(id=validated_data.get('user'))

        UsuarioAceito.objects.create(projeto=p, user=user, visualizou=False)

        p.convidados_set.remove(user)
        p.save()

        return {
            'success': 'Você aceitou o convite com sucesso',
            'project': validated_data.get('project'),
            'user': validated_data.get('user')
        }

    def update(self, instance, validated_data):
        return instance


class DeclineInviteSerializer(serializers.Serializer):
    class Meta:
        fields = ('success',)
        write_only_field = ('project', 'user',)

    project = serializers.IntegerField()
    user = serializers.IntegerField()

    success = serializers.CharField(max_length=500, required=False)
    error = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):
        attrs = super(DeclineInviteSerializer, self).validate(attrs)
        try:
            user: User = self.context.get('request').user
            p = Projeto.objects.get(id=attrs.get('project'))

            convidados = [u.id for u in p.convidados.all()]
            banidos = [u.id for u in p.banidos.all()]
            recusados = [u.id for u in p.recusados.all()]

            if user.id not in convidados:
                raise ValidationError(detail={'error': 'Você não foi convidado para este projeto'})

            if user.id in banidos or user.id in recusados:
                raise ValidationError(detail={'error': 'Você não pode aceitar solicitações neste projeto'})

        except Projeto.DoesNotExist:
            raise ValidationError(detail={'error': 'Este projeto não existe'})
        except User.DoesNotExist:
            raise ValidationError(detail={'error': 'Este usuário não existe'})

        return attrs

    def create(self, validated_data):
        p = Projeto.objects.get(id=validated_data.get('project'))
        user = User.objects.get(id=validated_data.get('user'))

        UsuarioConviteRecusado.objects.create(projeto=p, user=user, visualizou=True)

        p.convidados_set.remove(user)
        p.save()

        return {
            'success': 'Você recusou o convite com sucesso',
            'project': validated_data.get('project'),
            'user': validated_data.get('user')
        }

    def update(self, instance, validated_data):
        return instance