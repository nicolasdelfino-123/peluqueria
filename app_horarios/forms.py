from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'apellido_cliente', 'telefono_cliente']

from django import forms
from .models import Turno


class ReservaForm(forms.ModelForm):
    turno_id = forms.IntegerField(widget=forms.HiddenInput())
    fecha_seleccionada = forms.CharField(widget=forms.HiddenInput())
    turno_periodo = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'apellido_cliente', 'telefono_cliente']
        labels = {
            'nombre_cliente': 'Nombre',
            'apellido_cliente': 'Apellido',
            'telefono_cliente': 'Teléfono'
        }

    def __init__(self, *args, **kwargs):
        turno_id = kwargs.pop('turno_id', None)
        fecha_seleccionada = kwargs.pop('fecha_seleccionada', None)
        turno_periodo = kwargs.pop('turno_periodo', None)
        super().__init__(*args, **kwargs)
        if turno_id:
            print(f"Inicializando turno_id con: {turno_id}")
            self.fields['turno_id'].initial = turno_id
        if fecha_seleccionada:
            print(f"Inicializando fecha_seleccionada con: {fecha_seleccionada}")
            self.fields['fecha_seleccionada'].initial = fecha_seleccionada
        if turno_periodo:
            print(f"Inicializando turno_periodo con: {turno_periodo}")
            self.fields['turno_periodo'].initial = turno_periodo
