from django.db import models
from django.db.models import Model 
from django.utils.dateparse import parse_date
import re
import bcrypt
import datetime
# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or len(postData['first_name']) > 60:
            errors['first_name'] = 'First Name must be between 2 and 60 characters'
        if len(postData['last_name']) < 2 or len(postData['last_name']) > 60:
            errors['last_name'] = 'Last Name must between 2 and 60 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = User.objects.filter(email=postData['email'])
        if len(email_check) > 0:
            errors['email'] = "Email already in use"
        if postData['password'] != postData['confirm']:
            errors['password'] = "Confirmed password doesn't match"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        return errors

    def log_validator(self, postData):
        errors = {}
        email_check = User.objects.filter(email=postData['email'])
        print(email_check)
        if len(email_check) == 0:
            errors['email'] = "Incorrect email"
        elif not bcrypt.checkpw(postData['password'].encode(), email_check[0].password.encode()):
            errors['password'] = "Email and password do not match"
        return errors


class VillainManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = "Name can't be empty!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

 
class Villain(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    interests = models.CharField(max_length=45)
    villain_img = models.ImageField(upload_to="images/", null=True, blank=True)
    user_villain = models.ForeignKey(User, related_name="user_adds_villain", on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="user_likes_villain")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = VillainManager()