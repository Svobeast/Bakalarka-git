from django import forms

class Hod_kostkou(forms.Form):
    pocet = forms.IntegerField(label="Zadej počet hodů", min_value=1)