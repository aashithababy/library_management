from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile, Address

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    # Additional fields for address
    house_number_or_lane = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=255, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=255, required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        # Additional validation to ensure username contains only alphanumeric characters
        if not username.isalnum():
            raise ValidationError("Username must only contain letters and numbers.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        # Ensure first name only contains alphabetic characters
        if not first_name.isalpha():
            raise ValidationError("First name must only contain alphabetic characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        # Ensure last name only contains alphabetic characters
        if not last_name.isalpha():
            raise ValidationError("Last name must only contain alphabetic characters.")
        return last_name

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one alphabet.")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise ValidationError("The passwords do not match.")
        return confirm_password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Phone number must contain exactly 10 digits.")
        return phone_number

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        address = Address.objects.create(
            house_number_or_lane=self.cleaned_data.get('house_number_or_lane', ''),
            city=self.cleaned_data.get('city', ''),
            state=self.cleaned_data.get('state', ''),
            postal_code=self.cleaned_data.get('postal_code', ''),
            country=self.cleaned_data.get('country', ''),
        )
        UserProfile.objects.create(
            user=user,
            address=address,
            phone_number=self.cleaned_data['phone_number'],
        )
