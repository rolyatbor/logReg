# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def add_user(self, data):
        errors = []
        if not data['first']:
            errors.append('First name is required!')
        if not data['first'].isalpha():
            errors.append('First name must have alpha characters only!')
        if len(data['first']) < 2:
            errors.append('First Name must be at least 2 characters long.')
        if not data['last']:
            errors.append('Last name is required!')
        if not data['last'].isalpha():
            errors.append('Last name must have alpha characters only!')
        if len(data['last']) < 2:
            errors.append('Last Name must be at least 2 characters long.')
        if not EMAIL_REGEX.match(data['email']):
            errors.append('A valid email is required.')
        if len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long.')
        if data['password'] != data['confirm']:
            errors.append('Password did not match Confirm')
        if self.filter(email=data['email']):
            errors.append('Email already exists')

        response = {}

        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            response['status'] = True
            hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            user = self.create(first = data['first'], last = data['last'], email = data['email'], password = hashed_password)
            response['user'] = user
        return response
    def check_user(self, data):
        user = self.filter(email=data['email'])
        response = {}
        if user:
            if bcrypt.checkpw(data['password'].encode(), user[0].password.encode()):
                response['status'] = True
                response['user'] = user[0]
            else:
                response['status'] = False
                response['errors'] = 'Invalid email/password combination.'
        else:
            response['status'] = False
            response['errors'] = 'Email does not exist'
        return response
        
class User(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()