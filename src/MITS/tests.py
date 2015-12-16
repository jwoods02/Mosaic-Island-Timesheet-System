from django.test import TestCase
from django.contrib.auth.models import User

class CustomRegistrationTests(TestCase):
    """
    Tests to ensure custom registration subclass.
    """
    def create_valid_user_test(self):
        """
        User with valid and unique data should be created successfully
        :return:
        """


    def create_user_with_invalid_email_test(self):
        """
        User with non '@mosaicisland.com' email should be rejected
        :return:
        """


    def create_user_without_unique_email_test(self):
        """
        User without unique email should be rejected
        :return:
        """

