from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token

USER = get_user_model()


class EmptySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=1024, required=True)
    details = serializers.ListField(child=serializers.CharField(max_length=1024), required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# noinspection PyMethodMayBeStatic
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_2 = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PasswordResetConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_2 = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = '__all__'
        read_only_fields = ('date_joined', 'is_active')


# noinspection PyMethodMayBeStatic
class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        token = Token.objects.get_or_create(user=obj)[0]
        return token.key

    class Meta:
        model = USER
        fields = ('id', 'email', 'first_name', 'last_name', 'auth_token', 'date_joined', 'phone_number')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'auth_token', 'date_joined', 'phone_number')


# noinspection PyMethodMayBeStatic
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if USER.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already taken. Please provide a unique email.')
        return value

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
