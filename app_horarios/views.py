from django.shortcuts import render, redirect
from .models import Turno
from .forms import TurnoForm, ReservaForm
from datetime import datetime, time, timedelta
from twilio.rest import Client
from django.http import HttpResponseServerError
from django.utils import timezone
import calendar
from django.contrib import messages


from datetime import datetime, time
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Turno
from .forms import ReservaForm

def index(request):
    print("Método de la solicitud:", request.method)
    print("Contenido de request.POST:", request.POST)
    turnos = []
    fecha_seleccionada = None
    turno_periodo = ''  # Valor por defecto
    reserva_form = None

    if request.method == 'POST':
        print("Entrando en el bloque POST")
        # Caso 1: Selección de fecha
        if 'mostrarHorariosBtn' in request.POST:
            print("Caso 1: Selección de fecha")
            fecha_seleccionada = request.POST.get('fecha_seleccionada')
            turno_periodo = request.POST.get('turno_periodo', '')
            print(f"Fecha seleccionada: {fecha_seleccionada}, Turno periodo: {turno_periodo}")

            if fecha_seleccionada:
                try:
                    fecha = datetime.strptime(fecha_seleccionada, '%d-%m-%Y').date()
                    crear_turnos_si_no_existen(fecha)

                    if turno_periodo == 'manana':
                        turnos = Turno.objects.filter(
                            fecha=fecha,
                            hora__gte=time(8, 30),
                            hora__lt=time(12, 0),
                            disponible=True
                        ).order_by('hora')
                    else:  # turno_periodo == 'tarde'
                        turnos = Turno.objects.filter(
                            fecha=fecha,
                            hora__gte=time(16, 0),
                            hora__lt=time(21, 0),
                            disponible=True
                        ).order_by('hora')
                    print(f"Turnos encontrados: {turnos}")

                except ValueError:
                    messages.error(request, "Formato de fecha inválido. Por favor, seleccione una fecha válida.")
                    return redirect('index')

        # Caso 2 y 3: Selección de turno y Confirmación de reserva
        elif 'turno_id' in request.POST:
            print("Caso 2 o 3: Selección de turno o Confirmación de reserva")
            turno_id = request.POST.get('turno_id')
            fecha_seleccionada = request.POST.get('fecha_seleccionada', fecha_seleccionada)
            turno_periodo = request.POST.get('turno_periodo', turno_periodo)
            print(f"Turno ID seleccionado: {turno_id} para el periodo {turno_periodo} la fecha {fecha_seleccionada}")

            if turno_id:
                try:
                    turno = Turno.objects.get(id=turno_id)
                    
                    # Si 'confirmar_reserva' está en POST, proceder con la confirmación
                    if 'confirmar_reserva' in request.POST:
                        print("Confirmando reserva")
                        reserva_form = ReservaForm(request.POST, instance=turno)
                        if reserva_form.is_valid():
                            reserva = reserva_form.save(commit=False)
                            reserva.disponible = False
                            reserva.save()
                            messages.success(request, "Gracias por su reserva. Su turno ha sido confirmado.")
                            print("Reserva confirmada.")
                            return redirect('index')
                        else:
                            messages.error(request, "Hay errores en el formulario de reserva. Por favor, corrija y vuelva a intentarlo.")
                            print(f"Errores en el formulario de reserva: {reserva_form.errors}")
                    else:
                        # Si no, solo mostrar el formulario de reserva
                        reserva_form = ReservaForm(
                            initial={
                                'turno_id': turno_id,
                                'fecha_seleccionada': fecha_seleccionada,
                                'turno_periodo': turno_periodo
                            },
                            instance=turno
                        )
                        print(f"Formulario de reserva generado para el turno: {turno}")

                except Turno.DoesNotExist:
                    messages.error(request, "El turno seleccionado no existe.")

    context = {
        'turnos': turnos,
        'fecha_seleccionada': fecha_seleccionada,
        'turno_periodo': turno_periodo,
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
    # Código para enviar mensaje por WhatsApp utilizando Twilio
    # Asegúrate de tener configurada tu cuenta de Twilio y los créditos disponibles
    account_sid = 'tu_account_sid'
    auth_token = 'tu_auth_token'
    client = Client(account_sid, auth_token)
    
    mensaje = f"Se ha confirmado su reserva para el turno el {turno.fecha.strftime('%d-%m-%Y')} a las {turno.hora.strftime('%H:%M')}. Gracias."
    
    try:
        message = client.messages.create(
            body=mensaje,
            from_='tu_numero_twilio',
            to='+543534793366'  # Reemplaza con el número de teléfono al que deseas enviar el mensaje
        )
        print(f"Mensaje enviado correctamente a {message.to}. SID: {message.sid}")
    except Exception as e:
        print(f"Error al enviar mensaje por WhatsApp: {str(e)}")


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







# views.py



def ver_turnos(request):
    # Obtener mes y año actuales, o los que se pasen como parámetros
    now = datetime.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))

    # Calcular el primer y último día del mes
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1])

    # Calcular el primer día que se muestra en el calendario (martes)
    first_day_of_week = first_day_of_month
    while first_day_of_week.weekday() != 1:  # 1 es martes
        first_day_of_week -= timedelta(days=1)

    # Crear una lista de días vacíos hasta el primer día del mes
    empty_days = []
    current_day = first_day_of_week
    while current_day < first_day_of_month:
        empty_days.append({})
        current_day += timedelta(days=1)

    # Generar lista de días del mes con turnos
    calendar_days = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        current_day = datetime(year, month, day)
        if current_day.weekday() in [1, 2, 3, 4, 5]:  # Martes a sábado
            # Filtrar turnos por día y hora (mañana y tarde)
            turnos_manana = Turno.objects.filter(fecha=current_day, hora__lt=datetime.strptime("12:00", "%H:%M"), disponible=True)
            turnos_tarde = Turno.objects.filter(fecha=current_day, hora__gte=datetime.strptime("12:00", "%H:%M"), disponible=True)
            
            calendar_days.append({
                'day': day,
                'month': month,
                'year': year,
                'turnos_manana': turnos_manana,
                'turnos_tarde': turnos_tarde,
            })

    # Obtener el nombre del mes actual
    current_month_name = first_day_of_month.strftime('%B')

    context = {
        'current_month': current_month_name,
        'current_year': year,
        'prev_month': (month - 1) if month > 1 else 12,
        'prev_year': year - 1 if month == 1 else year,
        'next_month': (month + 1) if month < 12 else 1,
        'next_year': year + 1 if month == 12 else year,
        'empty_days': empty_days,
        'calendar_days': calendar_days,
    }
    return render(request, 'ver-turnos.html', context)