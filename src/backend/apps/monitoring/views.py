from django.http.response import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from .models import TicketReport, Revision, ScheduledReview, Externuser
from django.http import HttpResponse
from apps.core.models import Workstation, Room
from apps.notification.models import Notif
from datetime import datetime, date , timedelta
from django.contrib.auth.models import User as dj_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import HttpResponse
from collections import Counter
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
import time

def notificationreport(pc):
    userlist = [] 
    notiflist = [] 
    users = dj_user.objects.all()
    for i in users:
        userlist.append(i.id)    
    for j in userlist:    
        notifi = Notif()
        notifi.user = dj_user.objects.get(pk = j)
        notifi.message = "Un Usuario ha reportado el equipo"+" "+pc.name
        notifi.date = datetime.now()
        notiflist.append(notifi)
    Notif.objects.bulk_create(notiflist)
    return True

def existuser(email):
    aux = 0
    useremail = Externuser.objects.all()
    for i in useremail:
        if i.email == email:
            aux=1
    if aux==0:        
        user = Externuser()
        user.email = email
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
        notificationreport(reportes.pc)
        return redirect ('gratitude')   
    if pc != 0:
        context['pc'] = Workstation.objects.get(pk=pc)        
    else:
        context['rooms'] = Room.objects.all().order_by('room_name')
        
    template_name = "form_reports.html"
    return render(request,template_name,context)



def getpc(request):
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
    lab = Room.objects.all()
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
    context = {'reports': reports, 'lab':lab}
    return render(request,template_name,context)

def updateticketstate(request,id):
    report = get_object_or_404(TicketReport, id=id)
    if request.method=='POST':
        ticket = TicketReport.objects.get(pk = report.id)
        ticket.state = request.POST['state']
        ticket.comment = request.POST['comment']
        ticket.date_comment = datetime.now()
        ticket.user = dj_user.objects.get(username = request.POST['user'])
        ticket.save()
        return redirect ('reports')
    template_name="updateticketstate.html"
    context = {'report':report}
    return render(request,template_name,context)

@login_required
def computer_management(request):
    if request.POST:
        request.session['Room']= request.POST['Room']
        room_obtenido = Room.objects.get(pk=request.session['Room'])
        return redirect('equipment_maintenance')
    request.session['Room'] = None
    date_now = date.today()
    Schedule = ScheduledReview.objects.all().filter(date_scheduled__date=date_now)
    l = []
    for i in Schedule:
        l.append(i.room.id)  
    lab = Room.objects.all().filter(pk__in=l).order_by('room_name')
    count_lab = lab.count()
    context={
        'lab':lab, 'count_lab': count_lab
    }
    template_name="computer_management.html"
    return render(request,template_name,context)

def equipment_maintenance(request):
    if request.session['Room'] is not None or 'Room' not in request.session:
        room_obtenido = Room.objects.get(pk =request.session['Room'])
        pc = Workstation.objects.all().filter(room=room_obtenido).order_by('name')     
        context={
            'Room': room_obtenido,
            'pc':pc
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
    i = 0
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
    Schedule = ScheduledReview.objects.all()
    s = ""
    for i in Schedule:
        if i.date_scheduled.date() == date_now:
            s = ScheduledReview.objects.get(date_scheduled__date=date_now,room=idr)  
    if s!="":        
        Schedule_id = s.id                  
    if request.method=='POST':
        rev = Revision()
        if Schedule_id != "":        
            rev.scheduled_review = ScheduledReview.objects.get(pk = Schedule_id)
        rev.pc = Workstation.objects.get( pk = id_pc)
        rev.monitor = request.POST['monitor']
        rev.mouse = request.POST['mouse']
        rev.keyboard = request.POST['keyboard']
        rev.cpu = request.POST['cpu']
        rev.SO = request.POST['so']
        rev.software = request.POST['sw']
        rev.observation = request.POST['observaciones']
        rev.user = dj_user.objects.get(username = request.POST['user'])
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
    rev = Revision.objects.all()
    lista_schedule = []
    for i in rev:
        if i.scheduled_review is not None:
            if i.scheduled_review.id not in lista_schedule:
                lista_schedule.append(i.scheduled_review.id)          
    schedule = ScheduledReview.objects.all().filter(pk__in=lista_schedule)
    page = request.GET.get('page', 1)
    paginator = Paginator (schedule, 10)
    try:
        sch = paginator.page(page)
    except PageNotAnInteger:
        sch = paginator.page(1)
    except EmptyPage:
        sch = paginator.page(paginator.num_pages)
    context = {'sch':sch}
    temaplate_name="selectreviewpc.html"
    return render(request,temaplate_name,context)    

def showpcreview(request):
    if request.session['id'] is not None or 'id' not in request.session:
        reviews = Revision.objects.all().filter(scheduled_review=request.session['id']).order_by('id')
        template_name = "showreviewpc.html"
        return render(request,template_name,{ 'reviews':reviews })        
    else:
        return('selectreviewpc')
        
def updatepcreview(request, id):
    edit_review = get_object_or_404(Revision, id=id)
    rev_id = request.GET['id']
    if request.method=='POST':
        rev = Revision.objects.get(pk = rev_id)
        rev.pc = Workstation.objects.get( pk = request.POST['pc'])
        rev.monitor = request.POST['monitor']
        rev.mouse = request.POST['mouse']
        rev.keyboard = request.POST['keyboard']
        rev.cpu = request.POST['cpu']
        rev.SO = request.POST['so']
        rev.software = request.POST['sw']
        rev.observation = request.POST['observaciones']
        rev.date_created = datetime.now()
        rev.user = dj_user.objects.get(username = request.POST['user'])
        rev.save()
        return redirect ('showreviewpc')
    context = {
        'edit_review':edit_review
    }
    template_name="updatepcreview.html"
    return render(request,template_name,context)
def selectdate(request):
    if request.POST:
        request.session['datestart'] = request.POST['datestart']
        request.session['dateending'] = request.POST['dateending']
        return redirect('generalreports')
    request.session['datestart'] = None
    request.session['dateending'] = None
    context={}
    template_name = "selectdate.html"
    return render(request,template_name,context)

def generalreports(request): 
    if request.session['datestart'] is not None or 'datestart' not in request.session:
        if request.session['dateending'] is not None or 'dateending' not in request.session:
            count_room_hardware = {}
            count_room_software = {}
            count_room_so = {}
            count_room_m_h = {}
            count_room_m_s = {}
            count_room_m_so = {}
            total_r = []
            total_m = []
            i= 1
            j=1
            review = Revision.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending'])) 
            for r in review:
                if r.monitor != "P" or r.mouse !="P" or r.keyboard !="P" or r.cpu !="P":
                    if r.pc.room.room_name not in count_room_m_h:
                        count_room_m_h[r.pc.room.room_name] = 0
                    count_room_m_h[r.pc.room.room_name] +=1
                    
                if r.software != "O":
                    if r.pc.room.room_name not in count_room_m_s:
                        count_room_m_s[r.pc.room.room_name] = 0
                    count_room_m_s[r.pc.room.room_name] +=1 
                    
                if r.SO != "O":
                    if r.pc.room.room_name not in count_room_m_so:
                        count_room_m_so[r.pc.room.room_name] = 0
                    count_room_m_so[r.pc.room.room_name] +=1
                    
                if r.monitor != "P" or r.mouse !="P" or r.keyboard !="P" or r.cpu !="P" or r.software != "O" or r.SO !="O":
                   total_m.append(j)                         
            reports = TicketReport.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending']))     
            for r in reports:
                if r.category=="Hardware":
                    if r.pc.room.room_name not in count_room_hardware:
                        count_room_hardware[r.pc.room.room_name] = 0
                    count_room_hardware[r.pc.room.room_name] +=1
                    total_r.append(i)
                elif r.category=="Software":
                    if r.pc.room.room_name not in count_room_software:
                        count_room_software[r.pc.room.room_name] = 0
                    count_room_software[r.pc.room.room_name] +=1
                    total_r.append(i)
                elif r.category=="Sistema Operativo":
                    if r.pc.room.room_name not in count_room_so:
                        count_room_so[r.pc.room.room_name] = 0
                    count_room_so[r.pc.room.room_name] +=1
                    total_r.append(i)
            reports_total = sum(total_r)
            maintenance_total= (sum(total_m))             
            context= {'count_room_hardware':count_room_hardware,
            'count_room_software':count_room_software,'count_room_so':count_room_so, 'count_room_m_h': count_room_m_h,
            'count_room_m_s':count_room_m_s, 'count_room_m_so':count_room_m_so, 'reports_total':reports_total,
            'maintenance_total':maintenance_total}
            template_name = "generalreports.html"
            return render(request,template_name,context)

def chart_report_lab(request):
    count_room = {}
    date = datetime.today()
    year = date.strftime("%Y")
    begin = year+'-01-01'
    end = year+'-12-31'
    reports = TicketReport.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending']))
    for r in reports:
        if r.pc.room.room_name not in count_room:
            count_room[r.pc.room.room_name] = 0
        count_room[r.pc.room.room_name] +=1
    label = count_room.keys()
    label = list(label)
    data = count_room.values()
    data = list(data)
    label.append("")
    data.append(0)
    return JsonResponse(data={'label': label, 'data': data,})

def chart_maintenance_lab(request):
    count_room = {}
    date = datetime.today()
    year = date.strftime("%Y")
    begin = year+'-01-01'
    end = year+'-12-31'
    review = Revision.objects.filter(date_created__range=(request.session['datestart'],request.session['dateending']))
    for r in review:
        if r.monitor != "P" or r.mouse !="P" or r.keyboard !="P" or r.cpu !="P":
            if r.pc.room.room_name not in count_room:
                count_room[r.pc.room.room_name] = 0
            count_room[r.pc.room.room_name] +=1
        elif r.SO == "F" or r.software == "F":
            if r.pc.room.room_name not in count_room:
               count_room[r.pc.room.room_name] = 0
            count_room[r.pc.room.room_name] +=1
        elif r.SO == "N" or r.software == "N":
            if r.pc.room.room_name not in count_room:
               count_room[r.pc.room.room_name] = 0
            count_room[r.pc.room.room_name] +=1            
    label = count_room.keys()
    label = list(label)
    data = count_room.values()
    data = list(data)
    label.append("")
    data.append(0)
    return JsonResponse(data={'label': label, 'data': data,})
