from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from . import serializers, string_constants
from .models import TokenManager

USER = get_user_model()


def get_error(error_message, error_list):
    raw_data = {
        'error': error_message,
        'details': error_list
    }
    return serializers.ErrorSerializer(raw_data).data


def get_error_details(error_dict):
    errors = []
    for item in error_dict.items():
        error_message = item[0] + ': '
        for e in item[1]:
            error_message += str(e)
        errors.append(error_message)
    return errors


def get_user_not_found_error():
    data = get_error(
        string_constants.INVALID_LOGIN_CREDENTIAL,
        ['The username and password do not match. Please try with a valid combination.']
    )
    return data


def reset_password(email, token, new_password, new_password_2):
    try:
        token = TokenManager.objects.get(key=token, email=email)
        user = USER.objects.get(email=email)
        if new_password != new_password_2:
            data = get_error(
                string_constants.NEW_PASSWORD_MISMATCH,
                ['Please provide same password for both new password fields.']
            )
        else:
            if token.validate_token():
                user.set_password(new_password)
                user.save()
                data = {'detail': 'Success! Password reset successful. Please login with your new password.'}
            else:
                data = get_error(
                    string_constants.TOKEN_INVALID,
                    ['The code you provided has expired. Please request a new one.']
                )
    except ObjectDoesNotExist:
        data = get_error(
            string_constants.TOKEN_INVALID,
            ['The code you provided is invalid. Please provide a valid code.']
        )
    return data
