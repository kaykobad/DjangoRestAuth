from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible()
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^(01){1}[0-9]{9}$'
    message = 'Enter a valid phone number starting with 01.'
    flags = 0
