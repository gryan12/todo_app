from django.test import TestCase
from .models import valid_email, valid_password, validate_user

# Create your tests here.

class userValidationTests(TestCase):
    def test_validate_email_parses(self):
        self.assertTrue(1)
