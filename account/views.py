from django.contrib.auth import authenticate, logout, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers, utils, string_constants
from .models import TokenManager
from .utils import get_error, get_error_details

USER = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer

    @action(methods=['POST', ], detail=False, url_path='login')
    def login(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user is None:
                data = utils.get_user_not_found_error()
            else:
                data = serializers.AuthUserSerializer(user).data
        else:
            data = get_error(string_constants.INVALID_REQUEST_FORMAT, get_error_details(serializer.errors))

        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ], url_path='logout')
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        data = {'detail': 'Success! You have been logged out.'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ], url_path='change-password')
    def change_password(self, request):
        serializer = serializers.PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if serializer.validated_data['new_password'] != serializer.validated_data['new_password_2']:
                data = get_error(
                    string_constants.NEW_PASSWORD_MISMATCH,
                    ['Please provide same password for both new password fields.']
                )
            else:
                request.user.set_password(serializer.validated_data['new_password'])
                request.user.save()
                data = {"detail": "Success! Password change successful!"}
        else:
            data = get_error(string_constants.INVALID_REQUEST_FORMAT, get_error_details(serializer.errors))
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, url_path='verify-email')
    def verify_email(self, request):
        serializer = serializers.VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            token = TokenManager.objects.create(email=serializer.validated_data['email'])
            token.send_email(subject="Email Verification", message=f"Your email verification code is: {token.key} \n\n This code expires in 24 hours.\n\n Thanks")
            data = {"success": "An email with a verification code is sent to the email."}
        else:
            data = get_error(string_constants.EMAIL_TAKEN, get_error_details(serializer.errors))
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, url_path='confirm-email-verification')
    def confirm_email_verification(self, request):
        serializer = serializers.ConfirmEmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenManager.objects.get(email=serializer.validated_data['email'], key=serializer.validated_data['verification_code'])
                if token.validate_token():
                    data = {'detail': 'Success! Email is verified.'}
                else:
                    data = get_error(
                        string_constants.TOKEN_INVALID,
                        ['The code you provided has expired. Please request a new one.']
                    )
            except ObjectDoesNotExist:
                data = get_error(string_constants.EMAIL_TOKEN_MISMATCH, get_error_details(serializer.errors))
        else:
            data = get_error(string_constants.EMAIL_TOKEN_MISMATCH, get_error_details(serializer.errors))
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='register')
    def register(self, request):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            obj = USER.objects.create_user(**serializer.validated_data)
            # TODO: Update these two methods in account.User model
            obj.email_user(subject="Registration Successful!", message=f"Congrats {obj.first_name}!\n\nYour registration is successful! \n\nThanks")
            # obj.send_sms()
            data = serializers.AuthUserSerializer(obj).data
        else:
            data = get_error(string_constants.INVALID_REQUEST_FORMAT, get_error_details(serializer.errors))
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='reset-password')
    def reset_password(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            receiver_email = serializer.validated_data['email']
            if USER.objects.filter(email=receiver_email).exists():
                token = TokenManager.objects.create(email=receiver_email)
                token.send_email(subject="Password Reset Request", message=f"Your password reset code is: {token.key} \n\n This code expires in 24 hours.\n\n Thanks")

            data = {'detail': 'Success! You will receive an email shortly if you are registered. Check your inbox for password reset token.'}
        else:
            data = get_error(string_constants.INVALID_REQUEST_FORMAT, get_error_details(serializer.errors))
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='confirm-password-reset')
    def reset_password_confirmation(self, request):
        serializer = serializers.PasswordResetConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            receiver_email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            new_password_2 = serializer.validated_data['new_password_2']
            data = utils.reset_password(receiver_email, token, new_password, new_password_2)
        else:
            data = get_error(string_constants.INVALID_REQUEST_FORMAT, get_error_details(serializer.errors))
        return Response(data=data, status=status.HTTP_200_OK)
