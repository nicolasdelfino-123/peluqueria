# app_horarios/views.py

from django.shortcuts import render,redirect
from .models import Turno
from .forms import TurnoForm
from django.db.models import Q
from datetime import datetime, time

def index(request):
    turnos = []
    fecha_seleccionada = None  # Inicializa fecha_seleccionada como None al principio

    if request.method == 'POST':
        fecha_seleccionada = request.POST.get('fecha_seleccionada')
        turno_periodo = request.POST.get('turno_periodo', 'manana')  # por defecto muestra la mañana
        if fecha_seleccionada:
            try:
                fecha = datetime.strptime(fecha_seleccionada, '%d-%m-%Y').date()
            except ValueError:
                fecha = None
            
            if fecha:
                if turno_periodo == 'manana':
                    # Filtrar por la mañana (8:30 - 12:00)
                    turnos = Turno.objects.filter(
                        fecha=fecha,
                        hora__gte=time(8, 30),
                        hora__lt=time(12, 0)
                    ).order_by('hora')
                else:  # turno_periodo == 'tarde'
                    # Filtrar por la tarde (16:00 - 21:00 martes a viernes, 17:30 - 20:30 sábados)
                    turnos = Turno.objects.filter(
                        fecha=fecha,
                        hora__gte=time(16, 0),
                        hora__lt=time(21, 0)
                    ).exclude(
                        Q(fecha__week_day=6, hora__lt=time(17, 30)) |
                        Q(fecha__week_day=6, hora__gte=time(20, 30))
                    ).order_by('hora')
        else:
            turnos = Turno.objects.none()  # No se muestra ningún horario si no se proporciona fecha

    # Si no es un POST, simplemente se renderiza la página con turnos vacíos
    return render(request, 'index.html', {'turnos': turnos, 'fecha_seleccionada': fecha_seleccionada})


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
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirige a la página principal de horarios
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'editar_turno.html', {'form': form, 'turno': turno})
