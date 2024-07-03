# app_horarios/forms.py
from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['cliente', 'fecha', 'hora', 'servicio']

class TurnoEditForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['cliente', 'fecha', 'hora', 'servicio']

    def __init__(self, *args, **kwargs):
        super(TurnoEditForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].widget.attrs['readonly'] = True  # Ejemplo de campo solo lectura
