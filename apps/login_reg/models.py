from __future__ import unicode_literals

from django.db import models
import re , bcrypt

NO_NUM_REGEX = re.compile(r'^[^0-9]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def register(self,post_data):
        error_msgs = []
        if len(post_data['name']) < 2:
            error_msgs.append('Name is too short')
        elif not NO_NUM_REGEX.match(post_data['name']):
            error_msgs.append('Theres numbers in name')
        if not NO_NUM_REGEX.match(post_data['alias']):
            error_msgs.append('There are numbers in alias')
        if not EMAIL_REGEX.match(post_data['email']):
            error_msgs.append('Email is not valid')
        if len(post_data['password']) < 8:
            error_msgs.append('Password is too short')
        if post_data['password'] != post_data['cpassword']:
            error_msgs.append('Password does not match')
        if error_msgs:
            return {'error' : error_msgs}
        else:
            password = post_data['password']
            pwhash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            user = User.objects.create(name=post_data['name'],alias=post_data['alias'],email=post_data['email'],password=pwhash)
            return {'the_user' : user}

    def login(self,post_data):
        error_msgs = []
        user = User.objects.get(email=post_data['email'])
        password = user.password
        if bcrypt.hashpw(post_data['password'].encode('utf-8'), password.encode('utf-8')) == password:
            return {'the_user' : user}
        else:
            error_msgs.append('Incorrect password')
            return {'error' : error_msgs}

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    rating = models.IntegerField()
    review = models.CharField(max_length=255)
    book = models.ForeignKey(Book, related_name='reviews')
    user = models.ForeignKey(User, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
