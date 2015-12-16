from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm
from registration.users import UserModel

User = UserModel()


class RegistrationFormMIEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which only allows registration with
    mosaic island email addresses (and gmail.com for testing purposes)
    """

    good_domains = ['mosaicisland.com', 'gmail.com']

    def clean_email(self):

        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain not in self.good_domains:
            raise forms.ValidationError(_(
                "Only Mosaic Island e-mail addresses can be used. Please supply an 'example@mosaicisland.com' formatted email address. "))

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']
