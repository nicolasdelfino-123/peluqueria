from django.shortcuts import render, redirect
from .models import Turno
from .forms import TurnoForm, TurnoEditForm

def index(request):
    turnos = Turno.objects.all()
    return render(request, 'index.html', {'turnos': turnos})

def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirige a la página principal de horarios
    else:
        form = TurnoForm()
    return render(request, 'crear_turno.html', {'form': form})

def editar_turno(request, turno_id):
    turno = Turno.objects.get(pk=turno_id)
    if request.method == 'POST':
        form = TurnoEditForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirige a la página principal de horarios
    else:
        form = TurnoEditForm(instance=turno)
    return render(request, 'editar_turno.html', {'form': form, 'turno': turno})
