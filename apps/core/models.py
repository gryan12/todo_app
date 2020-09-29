import regex as re
from django.db import models
import logging
import os
import hashlib

# Create your models here.

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
    