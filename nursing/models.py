from django.db import models

# The model we'll create is based on the form fields we have: name, last name, age and email


class UserApplication(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()

    # A new field for text
    about_me = models.TextField(null=True, blank=True)

    # And a new one for the translated text
    about_me_translated = models.TextField(null=True, blank=True)
