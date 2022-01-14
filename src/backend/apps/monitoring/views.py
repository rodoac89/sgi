from django.http.response import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from .models import TicketReport, Revision, ScheduledReview, Externuser
from django.http import HttpResponse
from apps.core.models import Workstation, Room, Campus
from apps.notification.models import Notif
from django.contrib.auth.models import User as dj_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
import time
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

def notificationreport(pc):
    userlist = dj_user.objects.all().values_list('id',flat=True).distinct() 
    notiflist = [] 
    for j in userlist:    
        notifi = Notif()
        notifi.user = dj_user.objects.get(pk = j)
        notifi.message = "Un Usuario ha reportado el equipo"+" "+pc.name
        notifi.date = datetime.now()
        notifi.url = "reports"
        notiflist.append(notifi)
    Notif.objects.bulk_create(notiflist)
    return True

def existuser(useremail):
    if Externuser.objects.filter(email=useremail).exists():
        return False
    else:
        user = Externuser()
        user.email = useremail
        user.save()
    return True    

def form_reports(request, pc = 0):
    context = {}  
    if request.method=='POST':
        existuser(request.POST['email'])
        reportes = TicketReport()
        reportes.email = Externuser.objects.get(email = request.POST['email'])
        reportes.pc = Workstation.objects.get(pk = request.POST['Pc'])
        reportes.category = request.POST['category']
        reportes.description = request.POST['description']
        reportes.save()
        subject = f'[Reporte Generado] Comprobante de ticket generado N°{reportes.id}'
        message = f"Hola,\nGracias por contactarnos, tu reporte ha sido resivido exitosamente.\nEl número de reporte es: {reportes.id}\nSi deseas ver el estado actual de este ticket, ingresa al siguiente enlace {request.build_absolute_uri(reverse('searchreport', kwargs={}))} y en el campo de búsqueda ingresa el numero correspondiente.\n\n--\nEquipos de Laboratorios"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [reportes.email, ]
        send_mail( subject, message, email_from, recipient_list )
        
        notificationreport(reportes.pc)
        return redirect ('gratitude')   
    if pc != 0:
        context['pc'] = Workstation.objects.get(pk=pc)        
    else:
        context['campus'] = Campus.objects.all().order_by('name')
    template_name = "form_reports.html"
    return render(request,template_name,context)

def getroom(request):
    data = {}
    if request.method == "POST":
        campus_id = request.POST['campus_id']
        try:
            campus_name = Campus.objects.filter(pk = campus_id).first()
            room = Room.objects.filter(campus = campus_name).order_by('room_name')
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(room.values('id', 'room_name')), safe = False)

def getpc(request):
    data = {}
    if request.method == "POST":
        room_id = request.POST['room_id']
        try:
            room_name = Room.objects.filter(pk = room_id).first()
            pc = Workstation.objects.filter(room = room_name).order_by('name')
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(pc.values('id', 'name')), safe = False) 

def email_autocomplete(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    user = Externuser.objects.filter(email__icontains=q)
    results = []
    for i in user:
      email_json = {}
      email_json = i.email
      results.append(email_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

@login_required
def reports(request):
    reportes = TicketReport.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator (reportes, 10)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    template_name="reports.html"
    context = {'reports': reports}
    return render(request,template_name,context)

def updateticketstate(request,id):
    report = get_object_or_404(TicketReport, id=id)
    if request.method=='POST':
        ticket = TicketReport.objects.get(pk = report.id)
        ticket.state = request.POST['state']
        ticket.comment = request.POST['comment']
        ticket.date_comment = datetime.now()
        ticket.user = dj_user.objects.get(pk = request.user.id)
        ticket.save()
        subject = f'[Reporte Actualizado] Ticket actualizado N°{ticket.id}'
        message = f"Hola,\nTe contamos que tu reporte ha recibido una actualización.\nEl número de reporte es: {ticket.id}\nEstado ticket: {ticket.state}\nMensaje publicado el {ticket.date_comment}: {ticket.comment}\nSi deseas ver el estado actual de este ticket, ingresa al siguiente enlace {request.build_absolute_uri(reverse('searchreport', kwargs={}))} y en el campo de búsqueda ingresa el numero correspondiente.\n\n--\nEquipos de Laboratorios"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [ticket.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return redirect ('reports')
    template_name="updateticketstate.html"
    context = {'report':report}
    return render(request,template_name,context)

def searchreport(request):
    result = request.GET.get('search')
    report = TicketReport.objects.filter(pk = result).first()
    context = {'report':report }
    template_name = "searchreport.html"
    return render(request,template_name,context)

@login_required
def computer_management(request):
    if request.POST:
        request.session['Room']= request.POST['Room']
        return redirect('equipment_maintenance')
    request.session['Room'] = None
    date_now = date.today()
    schedule_room =  ScheduledReview.objects.all().filter(date_scheduled__date=date_now).order_by('room')
    count_lab = schedule_room.count()
    context={
        'count_lab': count_lab, 'schedule_room':schedule_room
    }
    template_name="computer_management.html"
    return render(request,template_name,context)

def equipment_maintenance(request):
    if request.session['Room'] is not None or 'Room' not in request.session:
        room_obtenido = Room.objects.get(pk =request.session['Room'])
        schedule_today = ScheduledReview.objects.filter(date_scheduled__date=date.today(),room=room_obtenido).first()
        review = Revision.objects.filter(scheduled_review=schedule_today).values_list('pc',flat=True).distinct()
        prev = Workstation.objects.filter(room=room_obtenido,id__in=review).order_by('name')
        notrev = Workstation.objects.all().filter(room=room_obtenido).exclude(id__in=review).order_by('name') 
        context={
            'Room': room_obtenido, 'pcnotrev':notrev, 'pcrev':prev
        }
        template_name="equipment_maintenance.html"
        return render(request,template_name,context)
    else:
        return redirect('computer_management')

def gratitude(request):
    template_name="gratitude.html"
    context={}
    return render(request,template_name,context)

def create_bulk_schedule_review(title, date_start_review, date_end_review, room):
    date_start = datetime.strptime(date_start_review, '%Y-%m-%dT%H:%M')
    date_finish = datetime.strptime(date_end_review, '%Y-%m-%dT%H:%M')
    weekDay = date_start.strftime('%w')
    review_dates = [date_start + timedelta(days=x) for x in range((date_finish-date_start).days + 1) if (date_start + timedelta(days=x)).weekday() == time.strptime(weekDay, '%w').tm_wday]
    schedules_review = []
    for rd in review_dates:
        schedulere = ScheduledReview()
        schedulere.date_scheduled = rd
        schedulere.title = title
        schedulere.room = Room.objects.get( pk = room)
        schedules_review.append(schedulere)
    ScheduledReview.objects.bulk_create(schedules_review)
    return False

def create_schedule_review(title, date_review, room):
    schedulere = ScheduledReview()
    schedulere.date_scheduled = date_review
    schedulere.title = title
    schedulere.room = Room.objects.get( pk = room)
    schedulere.save()
    return True

@login_required
def ShowScheduledReview(request):
    schedule = ScheduledReview.objects.all()
    room = Room.objects.all()
    if request.POST: 
        if 'recurrent' in request.POST:
            create_bulk_schedule_review(request.POST['title'], request.POST['date'], request.POST['dateend'], request.POST['room'])
        else:            
            create_schedule_review(request.POST['title'], request.POST['date'], request.POST['room'])
        
        return redirect ('ScheduledReview')   
    context = {'room':room,
    'schedule':schedule }
    template_name="ScheduledReview.html"
    return render(request,template_name,context)

def pcreview(request, id_pc):
    room_pc = Workstation.objects.get(pk=id_pc)
    idr = room_pc.room.id
    id_pc = room_pc.id
    date_now = date.today()
    Schedule = ScheduledReview.objects.get(date_scheduled__date=date_now,room=idr)           
    if request.method=='POST':
        rev = Revision()
        if Schedule != "":        
            rev.scheduled_review = ScheduledReview.objects.get(pk = Schedule.id)
        rev.pc = Workstation.objects.get( pk = id_pc)
        rev.monitor = request.POST['monitor']
        rev.mouse = request.POST['mouse']
        rev.keyboard = request.POST['keyboard']
        rev.cpu = request.POST['cpu']
        rev.SO = request.POST['so']
        rev.software = request.POST['sw']
        rev.observation = request.POST['observaciones']
        rev.user = dj_user.objects.get(pk = request.user.id)
        rev.save()                     
        return redirect ('equipment_maintenance')
    context = {
        'pc':room_pc.name
    }
    template_name = "pcreview.html"
    return render(request,template_name,context)

@login_required
def selectreviewpc(request):
    if request.POST:
        request.session['id']= request.POST['id']
        return redirect('showreviewpc')
    request.session['id'] = None
    r = Revision.objects.all().values_list('scheduled_review', flat=True).distinct()
    schedule = ScheduledReview.objects.all().filter(pk__in=r).order_by('-date_scheduled')
    count_schedule = schedule.count()
    page = request.GET.get('page', 1)
    paginator = Paginator (schedule, 10)
    try:
        sch = paginator.page(page)
    except PageNotAnInteger:
        sch = paginator.page(1)
    except EmptyPage:
        sch = paginator.page(paginator.num_pages)
    context = {'sch':sch, 'count_schedule': count_schedule}
    temaplate_name="selectreviewpc.html"
    return render(request,temaplate_name,context)    

def showpcreview(request):
    if request.session['id'] is not None or 'id' not in request.session:
        reviews = Revision.objects.all().filter(scheduled_review=request.session['id']).order_by('pc')
        template_name = "showreviewpc.html"
        return render(request,template_name,{ 'reviews':reviews })        
    else:
        return('selectreviewpc')
        
def updatepcreview(request, id):
    pc = Workstation.objects.filter(pk=id).first()
    revi = Revision.objects.filter(date_created__date=date.today(),pc=pc.id).first()
    if revi is not None:
        edit_review = revi
    else:
        edit_review = get_object_or_404(Revision, id=id)
    if request.method=='POST':
        rev = Revision.objects.get(pk = edit_review.id)
        rev.pc = Workstation.objects.get( pk = edit_review.pc.id)
        rev.monitor = request.POST['monitor']
        rev.mouse = request.POST['mouse']
        rev.keyboard = request.POST['keyboard']
        rev.cpu = request.POST['cpu']
        rev.SO = request.POST['so']
        rev.software = request.POST['sw']
        rev.observation = request.POST['observaciones']
        rev.date_created = datetime.now()
        rev.user = dj_user.objects.get(pk = request.user.id)
        rev.save()
        if revi is not None:
            return redirect('equipment_maintenance')
        else:    
            return redirect ('showreviewpc')
    context = {
        'edit_review':edit_review
    }
    template_name="updatepcreview.html"
    return render(request,template_name,context)
@login_required
def selectdate(request):
    if request.POST:
        request.session['datestart'] = request.POST['datestart']
        request.session['dateending'] = request.POST['dateending']
        return redirect('generalreports')
    request.session['datestart'] = None
    request.session['dateending'] = None
    r = TicketReport.objects.all().values_list('pc')
    w = Workstation.objects.all().filter(id__in=r).values('room__room_name').annotate(count = Count('room'))
    context={}
    template_name = "selectdate.html"
    return render(request,template_name,context)

def generalreports(request): 
    if request.session['datestart'] is not None or 'datestart' not in request.session:
        if request.session['dateending'] is not None or 'dateending' not in request.session:
            #querys pc con problemas en revisión
            reviewmaintenancetotal = Revision.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending'])).exclude(monitor="P",mouse="P",keyboard="P",cpu="P",software="O",SO="O").count()
            reviewh = Revision.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending'])).exclude(monitor="P",mouse="P",keyboard="P",cpu="P").values_list('pc',flat=True)
            countroommh = Workstation.objects.filter(pk__in=reviewh).values('room__room_name').annotate(cantidad = Count('room'))
            reviews = Revision.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending'])).exclude(software="O").values_list('pc',flat=True)
            countroomms = Workstation.objects.filter(pk__in=reviews).values('room__room_name').annotate(cantidad = Count('room'))
            reviewso = Revision.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending'])).exclude(SO="O").values_list('pc',flat=True)
            countroommso = Workstation.objects.filter(pk__in=reviewso).values('room__room_name').annotate(cantidad = Count('room'))                           
            #querys reportes
            reports = TicketReport.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending'])).count()
            report_s = TicketReport.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending']),category="Software").values_list('pc',flat=True)
            countrooms = Workstation.objects.filter(pk__in=report_s).values('room__room_name').annotate(cantidad = Count('room'))
            report_so = TicketReport.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending']),category="Sistema Operativo").values_list('pc',flat=True)
            countroomso = Workstation.objects.filter(pk__in=report_so).values('room__room_name').annotate(cantidad = Count('room'))      
            reh = TicketReport.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending']),category="Hardware").values_list('pc',flat=True)
            coutnroomh = Workstation.objects.filter(pk__in=reh).values('room__room_name').annotate(cantidad = Count('room'))                
            context= {'reports':reports, 'reviewmaintenancetotal':reviewmaintenancetotal,'countroomh':coutnroomh, 'countrooms':countrooms,'countroomso':countroomso,'countroommh':countroommh,
                      'countroomms':countroomms, 'countroommso':countroommso}
            template_name = "generalreports.html"
            return render(request,template_name,context)

def chart_report_lab(request):
    report = TicketReport.objects.all().filter(date_created__range=(request.session['datestart'],request.session['dateending'])).values_list('pc',flat=True)
    countroom = Workstation.objects.filter(pk__in=report).values('room__room_name').annotate(cantidad = Count('room'))
    label = list(countroom.values_list('room__room_name',flat=True))
    data = list(countroom.values_list('cantidad',flat=True))
    label.append("")
    data.append(0)
    return JsonResponse(data={'label': label, 'data': data,})

def chart_maintenance_lab(request):
    review = Revision.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending'])).exclude(monitor="P",mouse="P",keyboard="P",cpu="P",software="O",SO="O").values_list('pc',flat=True)
    countroom = Workstation.objects.filter(pk__in=review).values('room__room_name').annotate(cantidad = Count('room'))
    label = list(countroom.values_list('room__room_name',flat=True))
    data = list(countroom.values_list('cantidad',flat=True))
    label.append("")
    data.append(0)
    return JsonResponse(data={'label': label, 'data': data,})
