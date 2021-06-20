from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)

    @classmethod
    def get_user(cls, instance: Profile):
        return {
            'username': instance.user.username,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'email': instance.user.email,
        }

    def create(self, validated_data: dict):
        user: User = self.context.get('request').user
        user.profile.interesses.set(validated_data.get('interesses', None))
        user.profile.descricao = validated_data.get('descricao', None)
        user.profile.mostrar_perfil = validated_data.get('mostrar_perfil', True)
        user.profile.save()

        return user.profile

    def update(self, instance: Profile, validated_data: dict):
        instance.descricao = validated_data.get('descricao', instance.descricao)
        instance.mostrar_perfil = validated_data.get('mostrar_perfil', instance.mostrar_perfil)
        instance.interesses.set(validated_data.get('interesses', instance.interesses.all()))
        instance.save()

        return instance


class SimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'descricao', 'interesses', 'invite_url', 'gratificado',
                  'advertencias', 'banido', 'perfil_classifier', 'first_name', 'last_name')
        read_only_fields = ('user',)

    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    invite_url = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_first_name(instance):
        return instance.user.first_name

    @staticmethod
    def get_last_name(instance):
        return instance.user.last_name

    @staticmethod
    def get_invite_url(instance):
        return instance.url_hash
