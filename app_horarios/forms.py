# app_horarios/forms.py
from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['cliente', 'fecha', 'hora', 'servicio']

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs['class'] = 'form-control'  # Añadir clases de Bootstrap u otras clases CSS necesarias
        self.fields['hora'].widget.attrs['class'] = 'form-control'   # Añadir clases de Bootstrap u otras clases CSS necesarias
