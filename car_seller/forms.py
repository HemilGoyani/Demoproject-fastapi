from tkinter.tix import Form
from django import forms
from .models import *


class CarSellersForm(forms.ModelForm):
    class Meta:
        model = CarSeller
        fields = '__all__'
