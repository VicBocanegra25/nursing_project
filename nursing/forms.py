from django import forms

# Using Validation Error to fix issues with the text fields
from django.core.exceptions import ValidationError


def validate_alphabetic(value):
    if not all(char.isalpha() or char.isspace() or char == "-" for char in value):
        raise ValidationError(
            f"{value} contains non-alphabetic characters",
            params={"value": value},
        )


class SubmitDataForm(forms.Form):
    name = forms.CharField(
        max_length=50, validators=[validate_alphabetic], label="First Name"
    )
    last_name = forms.CharField(
        max_length=50, validators=[validate_alphabetic], label="Last Name"
    )
    age = forms.IntegerField(min_value=0, max_value=100, label="Age")
    email = forms.EmailField(label="Email")
