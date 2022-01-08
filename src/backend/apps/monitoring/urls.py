from django.urls import path, include
from . import views
from django.conf.urls import url
urlpatterns = [

    path('form_reports/', views.form_reports, name="form_reports"),
    path('form_reports/<pc>/', views.form_reports, name="form_reports"),
    path('reports/', views.reports,name="reports"),
    path('computer_management/',views.computer_management,name="computer_management"),
    path('equipment_maintenance/',views.equipment_maintenance,name="equipment_maintenance"),
    path('gratitude/',views.gratitude,name="gratitude"),
    path('ScheduledReview/',views.ShowScheduledReview,name="ScheduledReview"),
    path('pcreview/<id_pc>',views.pcreview,name="pcreview"),
    path('showreviewpc/',views.showpcreview,name="showreviewpc"),
    path('email_autocomplete/',views.email_autocomplete,name="email_autocomplete"),
    path('updatepcreview/<int:id>/',views.updatepcreview,name="updatepcreview"),
    path('getpc/',views.getpc,name="getpc"),
    path('getroom/',views.getroom,name="getroom"),
    path('generalreports/',views.generalreports,name="generalreports"),
    path('chart_report_lab/',views.chart_report_lab,name="chart_report_lab"),
    path('selectreviewpc/',views.selectreviewpc,name="selectreviewpc"),
    path('chart_maintenance_lab/',views.chart_maintenance_lab,name="chart_maintenance_lab"),
    path('selectdate/',views.selectdate,name="selectdate"),
    path('updateticketstate/<int:id>/',views.updateticketstate,name="updateticketstate"),
    path('searchreport/',views.searchreport,name="searchreport"),
]