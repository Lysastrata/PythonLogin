from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters"
        if not re.match(EMAIL_REGEX, postData['email'] ):
            errors["email"] = "Email needs to be valid"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be 8 charcters or more"
        if postData['password'] != postData['confirmation']:
            errors['confirmation'] = 'Password has to match confirmation'
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
