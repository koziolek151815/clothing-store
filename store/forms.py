from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import forms, ModelForm

from store.models import Delivery


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = ['name', 'surname', 'city', 'phone', 'postal_code']
