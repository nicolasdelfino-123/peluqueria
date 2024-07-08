from django import forms
from .models import Turno

#este estaría sin uso para mi
class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'apellido_cliente', 'telefono_cliente']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'apellido_cliente', 'telefono_cliente']
        labels = {
            'nombre_cliente': 'Nombre',
            'apellido_cliente': 'Apellido',
            'telefono_cliente': 'Teléfono'
        }
        turno_id = forms.IntegerField(widget=forms.HiddenInput())

