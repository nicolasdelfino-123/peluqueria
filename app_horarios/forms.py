from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'apellido_cliente', 'telefono_cliente']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'apellido_cliente', 'telefono_cliente']


