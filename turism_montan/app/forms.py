from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recenzie, Traseu, PunctDeInteres, ZonaMontana, Marcaj

class BootstrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'

class RegisterForm(BootstrapForm, UserCreationForm):
    email = forms.EmailField(required=True, label="Adresa de email")

    class Meta:
        model = User
        fields = ("username", "email")
    
class RecenzieForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Recenzie
        fields = ["evaluare", "comentariu"]
        labels = {
            "evaluare": "Stele",
            "comentariu": "Impresia ta",
        }

        widgets = {
            "comentariu": forms.Textarea(attrs={'rows': 3}),
        }

class TraseuForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Traseu
        fields = [
            "nume_traseu", "zona", "dificultate", "durata_traseu", "distanta_km",
            "altitudine_maxima", "sezon_recomandat", "descriere", "marcaje", "puncte_interes"
        ]
        widgets = {
            "descriere": forms.Textarea(attrs={'rows': 4}),
            "marcaje": forms.SelectMultiple(),
            "puncte_interes": forms.SelectMultiple(),
        }

class ZonaMontanaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ZonaMontana
        fields = ["nume_zona", "regiune", "descriere", "imagine_reprezentativa"]
        widgets = {
            "descriere": forms.Textarea(attrs={'rows': 3}),
        }

class MarcajForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Marcaj
        fields = ["tip", "culoare", "imagine"]

class PuncteDeInteresForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = PunctDeInteres
        fields = [
            "nume_pct", "tip_pct", "zona", "descriere", "latitudine", "longitudine", "imagine" 
        ]
        widgets = {
            "descriere": forms.Textarea(attrs={'rows': 2}),
        }
