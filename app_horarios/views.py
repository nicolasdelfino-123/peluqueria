from django.shortcuts import render, redirect
from .models import Turno
from .forms import TurnoForm, ReservaForm
from django.db.models import Q
from datetime import datetime, time
from twilio.rest import Client

def index(request):
    turnos = []
    fecha_seleccionada = None
    mensaje_error = None
    mensaje_exito = None
    reserva_form = None

    if request.method == 'POST':
        if 'fecha_seleccionada' in request.POST:
            fecha_seleccionada = request.POST.get('fecha_seleccionada')
            turno_periodo = request.POST.get('turno_periodo', 'manana')
            
            if fecha_seleccionada:
                try:
                    fecha = datetime.strptime(fecha_seleccionada, '%d-%m-%Y').date()
                    
                    crear_turnos_si_no_existen(fecha)
                    
                    if turno_periodo == 'manana':
                        if fecha.weekday() < 5:  # Martes a Viernes
                            turnos = Turno.objects.filter(
                                fecha=fecha,
                                hora__gte=time(8, 30),
                                hora__lt=time(12, 0),
                                disponible=True
                            ).order_by('hora')
                        elif fecha.weekday() == 5:  # Sábado
                            turnos = Turno.objects.filter(
                                fecha=fecha,
                                hora__gte=time(8, 30),
                                hora__lt=time(13, 0),
                                disponible=True
                            ).order_by('hora')
                    else:  # turno_periodo == 'tarde'
                        if fecha.weekday() < 5:  # Martes a Viernes
                            turnos = Turno.objects.filter(
                                fecha=fecha,
                                hora__gte=time(16, 0),
                                hora__lt=time(21, 0),
                                disponible=True
                            ).order_by('hora')
                        elif fecha.weekday() == 5:  # Sábado
                            turnos = Turno.objects.filter(
                                fecha=fecha,
                                hora__gte=time(17, 30),
                                hora__lt=time(20, 30),
                                disponible=True
                            ).order_by('hora')
                    
                    if not turnos:
                        mensaje_error = "No hay horarios disponibles para la fecha y periodo seleccionados."
                except ValueError:
                    mensaje_error = "Formato de fecha inválido. Por favor, seleccione una fecha válida."
            else:
                mensaje_error = "Por favor, seleccione una fecha."
        elif 'turno_id' in request.POST:
            turno_id = request.POST.get('turno_id')
            turno = Turno.objects.get(id=turno_id)
            reserva_form = ReservaForm(instance=turno)
        elif 'confirmar_reserva' in request.POST:
            turno_id = request.POST.get('turno_id')
            turno = Turno.objects.get(id=turno_id)
            turno.disponible = False
            turno.save()
            enviar_mensaje_whatsapp(turno)
            mensaje_exito = "Reserva confirmada exitosamente. Se ha enviado un mensaje de WhatsApp con los detalles."
            turnos = []  # Limpiamos los turnos después de confirmar la reserva
            reserva_form = None
    
    context = {
        'turnos': turnos,
        'fecha_seleccionada': fecha_seleccionada,
        'mensaje_error': mensaje_error,
        'mensaje_exito': mensaje_exito,
        'reserva_form': reserva_form,
    }
    return render(request, 'index.html', context)

def crear_turnos_si_no_existen(fecha):
    if fecha.weekday() < 5:  # Martes a Viernes
        horarios_manana = [(8, 30), (9, 0), (9, 30), (10, 0), (10, 30), (11, 0), (11, 30)]
        horarios_tarde = [(16, 0), (16, 30), (17, 0), (17, 30), (18, 0), (18, 30), (19, 0), (19, 30), (20, 0), (20, 30)]
    elif fecha.weekday() == 5:  # Sábado
        horarios_manana = [(8, 30), (9, 0), (9, 30), (10, 0), (10, 30), (11, 0), (11, 30), (12, 0), (12, 30)]
        horarios_tarde = [(17, 30), (18, 0), (18, 30), (19, 0), (19, 30), (20, 0)]
    else:  # Domingo y Lunes
        return

    for hora, minuto in horarios_manana:
        Turno.objects.get_or_create(
            fecha=fecha,
            hora=time(hora, minuto),
            defaults={'disponible': True}
        )

    for hora, minuto in horarios_tarde:
        Turno.objects.get_or_create(
            fecha=fecha,
            hora=time(hora, minuto),
            defaults={'disponible': True}
        )

def enviar_mensaje_whatsapp(turno):
    account_sid = 'your_twilio_account_sid'
    auth_token = 'your_twilio_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"¡Reserva confirmada! Se ha agendado un turno para el día {turno.fecha.strftime('%d-%m-%Y')} a las {turno.hora.strftime('%H:%M')}.",
        from_='whatsapp:+14155238886',  # Twilio sandbox number
        to='whatsapp:+543534793366'  # Tu número de WhatsApp
    )

    print(message.sid)  # opcional, para ver el SID del mensaje

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
