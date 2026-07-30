from django.shortcuts import render, redirect

from .models import JobApplication, Event

from .forms import JobApplicationForm, EventForm

from django.shortcuts import get_object_or_404
 
from datetime import date as date_class

import calendar

from datetime import date

def application_list(request):
   applications = JobApplication.objects.all()
   return render(request, 'tracker/application_list.html', {'applications': applications})

def application_create(request):
   if request.method == 'POST':
      form = JobApplicationForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('application_list')
   else: 
      form = JobApplicationForm()

   return render(request, 'tracker/application_form.html' , {'form' : form})


def application_edit(request, pk):
   application = get_object_or_404(JobApplication, pk=pk)

   if request.method == 'POST':
      form = JobApplicationForm(request.POST, instance=application)

      if form.is_valid():
         form.save()
         return redirect('application_list')
   
   else:
         form = JobApplicationForm(instance=application)

   return render(request, 'tracker/application_form.html', {'form' : form, 'application' : application
})

def application_delete(request,pk):
    application = get_object_or_404(JobApplication, pk=pk)

    if request.method == 'POST':
       application.delete()
       return redirect('application_list')

    return render(request, 'tracker/application_confirm_delete.html', {'application': application})
 
def application_calendar(request,pk,year=None, month=None):
   application = get_object_or_404(JobApplication, pk=pk)

   today = date.today()
   year =year or today.year
   month =month or today.month

   cal = calendar.monthcalendar(year, month)
   month_name = calendar.month_name[month]
   
   if month == 1:
      prev_year, prev_month = year - 1, 12

   else:
      prev_year, prev_month = year, month - 1

   if month == 12:
      next_year, next_month = year + 1 , 1

   else:
      next_year, next_month = year, month + 1

   return render(request, 'tracker/application_calendar.html', {

   'application': application,
   'cal' : cal,
   'month_name' : month_name,
   'year' : year,
   'prev_year': prev_year,
   'prev_month': prev_month,
   'next_year': next_year,
   'next_month': next_month,
})


def calendar_view(request, year=None, month=None):
   today = date.today()
   year = year or today.year
   month = month or today.month
   
   events = Event.objects.filter(date__year=year,date__month=month)

   events_by_day = {}

   for event in events:
      day = event.date.day
      events_by_day.setdefault(day, []).append(event)

   month_days = calendar.monthcalendar(year, month)

   cal = []

   for week in month_days:
     week_data = []
     for day in week:
       if day == 0:
          week_data.append(None)
       else:
          week_data.append({'day':day, 'events': events_by_day.get(day, [])})
     cal.append(week_data)
   month_name = calendar.month_name[month]

    
   if month == 1:
      prev_year, prev_month = year - 1, 12
   else:
       prev_year, prev_month = year, month - 1

   if month == 12:
       next_year, next_month = year + 1, 1
   else:
       next_year, next_month = year, month + 1
   
   return render(request, 'tracker/calendar.html', {
      'cal': cal,
      'month_name' : month_name,
      'month': month,
      'year': year,
      'events_by_day': events_by_day,
      'prev_year': prev_year, 'prev_month': prev_month,
      'next_year': next_year, 'next_month': next_month,
})

def event_create(request,year,month,day):
   selected_date = date_class(year,month,day)
   
   if request.method == 'POST':
      form = EventForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('calendar')
   else:
      form = EventForm(initial={'date': selected_date})

   return render(request,'tracker/event_form.html', {'form': form, 'selected_date': selected_date})
