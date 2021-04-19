from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .mail import send_welcome_email, send_reset_password_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'is_admin')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        norm_email = value.lower()
        if get_user_model().objects.filter(email=norm_email).exists():
            raise serializers.ValidationError("user with this email address already exists.")
        return norm_email

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        send_welcome_email(user)
        return user

    def update(self, obj, validated_data):
        password = validated_data.pop('password', None)
        if password:
            obj.set_password(password)
        return super().update(obj, validated_data)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    '''
    Override AuthTokenSerializer to accept email field instead of username
    '''
    username = None
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )

    def validate(self, attrs):
        attrs['username'] = attrs['email'].lower()
        attrs = super().validate(attrs)
        del attrs['username']
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def create(self, validated_data):
        email = validated_data['email'].lower()
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return {}

        reset_token = default_token_generator.make_token(user)
        send_reset_password_email(user, reset_token=reset_token)

        return {}


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        token = validated_data['token']
        user_id = validated_data['user_id']
        password = validated_data['password']

        user = get_user_model().objects.get(id=user_id)
        if not default_token_generator.check_token(user, token):
            raise ParseError(detail='Invalid token')

        user.set_password(password)
        user.save()
        return {}
