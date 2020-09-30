import regex as re
from django.db import models
from django.contrib.auth.models import User
import logging
import os
import hashlib

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



def validate_user(username, p1, p2, email=None):
    if p1 != p2:
        logging.debug("passwords do not match")
        return False

    elif not valid_password(p1):
        return False

    elif email and not valid_email(email):
        return False

    return True

def valid_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not (re.search(regex, email)):
        return False

    return True


def user_exists(username, email):
    return True

def valid_password(password):
    return True
    