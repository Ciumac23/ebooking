from django import forms
from django.forms import ModelForm
from .models import Book, Room
class UserForm(forms.Form):
    first_name = forms.CharField(label="First name")
    second_name = forms.CharField(label="Last name")
    password1 = forms.CharField(label="Password", max_length=15, widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repeat password", max_length=15, widget=forms.PasswordInput())
    username = forms.CharField(label="User name")
    email = forms.CharField(label="@email")

    field_order = ["first_name", "second_name", "username", "password1", "password2", "email"]


class LoginForm(forms.Form):
    username = forms.CharField(label="User name")
    password = forms.CharField(label="Password", max_length=15, widget=forms.PasswordInput())


class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = '__all__'

class RoomForm(ModelForm):
	class Meta:
		model = Room
		fields = '__all__'