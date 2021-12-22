#from apps.core.views import index
from django.conf.urls import url, include
"""from django.urls.conf import path
from django.urls.resolvers import URLPattern

from apps.licenses.views import formulario"""
from django.urls import path, include
from .views import EnterLicensesView, SoftwareRequestView, adm_licencias, enter_licenses, form_info, form_info1, form_list, home, labs, equipos, pc, SoftwareRequestForm, prueba, reportes, software_request_done, form_index, forms_view, form_list, enter_licenses, form_info1, edit_license, delete_license, licenses_reports, search_license, search_form, status_form
urlpatterns = [
    path('', home, name = 'index' ),
    path('form_index/', form_index, name = 'form_index'),
    path('labs/', labs, name = 'labs'),
    path('adm_licencias/', adm_licencias, name = 'adm_licencias'),
    path('equipos/', equipos, name = 'equipos'),
    path('pc/', pc, name = 'pc'),
    #path('formulario_creado/', formulario, name = 'formulario_creado'),
    path('form_create/', SoftwareRequestView.form_create, name = 'form_create'),
    path('software_request_done/', software_request_done, name = 'software_request_done'),
    path('forms_view/', forms_view, name = 'forms_view'),
    path('form_list/', form_list, name = 'form_list'),
    path('search_form/', search_form, name = 'search_form'),
    path('enter_licenses/', enter_licenses, name = 'enter_licenses'),
    path('enter_license/', EnterLicensesView.enter_license, name = 'enter_license'),
    # path('info_license/', info_license, name = 'info_license'),
    path('form_info1/', form_info1, name = 'form_info1'),
    path('edit_license/<id>/', edit_license, name="edit_license"),
    path('delete_license/<id>/', delete_license, name="delete_license"),
    path('status_form/<id>/', status_form, name="status_form"),
    path('licenses_reports/', licenses_reports, name="licenses_reports"),
    path('search_license/', search_license, name="search_license"),
    path('prueba/', prueba, name="prueba"),
    path('reportes/', reportes, name="reportes"),

]