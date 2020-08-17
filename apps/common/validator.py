from django.core.exceptions import ValidationError

def validate_phone(value):
    valid = ['08', '07', '09']
    valid_no = value[:2]
    if valid_no not in valid:
        raise ValidationError("Please enter a valid phone number")
    if len(value) < 11:
        raise ValidationError('Phone number not complete')