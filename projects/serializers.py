from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Projeto, UsuarioAceito


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

        return {
            'success': 'Usuário aceito com sucesso',
            'project': validated_data.get('project'),
            'user': validated_data.get('user')
        }

    def update(self, instance, validated_data):
        return instance
