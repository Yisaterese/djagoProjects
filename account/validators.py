from rest_framework.exceptions import ValidationError


def validate_pin(pin:str):
    if len(pin) < 4:
        raise ValidationError("pin must be four digits")


