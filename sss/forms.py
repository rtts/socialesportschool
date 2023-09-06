from django import forms
from django.contrib.auth.models import User
from bootcamps.models import *

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='Voornaam')
    last_name = forms.CharField(label='Achternaam')
    email = forms.EmailField(label='Emailadres')
    password1 = forms.CharField(label='Kies een wachtwoord', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Herhaal het wachtwoord', widget=forms.PasswordInput)

    def clean(self):
        if User.objects.filter(username=self.data['email']).exists() or User.objects.filter(email=self.data['email']).exists():
            raise forms.ValidationError('Er bestaat al een account met dit emailadres. Kies een ander emailadres.')
        return super().clean()

    def save(self, commit=True):
        user = User(
            username = self.cleaned_data['email'],
            email = self.cleaned_data['email'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('De twee wachtwoorden komen niet met elkaar overeen')
        return password2

# class ZorginstellingForm(BaseRegistrationForm):
#     def create_org(self):
#         return ZorgLocatie(
#             name = self.cleaned_data['org'],
#             street = self.cleaned_data['street'],
#             number = self.cleaned_data['number'],
#             zipcode = self.cleaned_data['zipcode'],
#             city = self.cleaned_data['city'],
#             website = self.cleaned_data['website'],
#         )

# class SportschoolForm(BaseRegistrationForm):
#     def create_org(self):
#         return Sportschool(
#             name = self.cleaned_data['org'],
#             street = self.cleaned_data['street'],
#             number = self.cleaned_data['number'],
#             zipcode = self.cleaned_data['zipcode'],
#             city = self.cleaned_data['city'],
#             website = self.cleaned_data['website'],
#         )

# class ChangeDetails(forms.Form):
#     org = forms.CharField(label='Naam van de organisatie')
#     first_name = forms.CharField(label='Voornaam contactpersoon')
#     last_name = forms.CharField(label='Achternaam contactpersoon')
#     email = forms.EmailField(label='Emailadres contactpersoon')
#     # phone = forms.CharField(label='Telefoonnummer', required=False)
#     website = forms.CharField(label='Website', initial='http://', required=False)

#     password1 = forms.CharField(label='Uw oude wachtwoord', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Uw nieuwe wachtwoord', widget=forms.PasswordInput)
#     password3 = forms.CharField(label='Herhaal nieuwe wachtwoord', widget=forms.PasswordInput)
