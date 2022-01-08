"""from Labs.backend.apps.licenses.models import form_software"""

from datetime import datetime, timedelta
from apps.licenses.forms import SoftwareRequestForm, EnterLicensesForm
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import LicensesList, SoftwareForm


def home(request):
    return render(request, "index.html")


# ------FORMULARIOS------ #


def form_index(request):
    form = SoftwareRequestForm()
    return render(request, "formulario.html", {"form": form})


def forms_view(request):
    context = {}

    if request.GET:
        if "id_user" in request.GET:
            data_forms = SoftwareForm.objects.get(
                id_request=int(request.GET["id_user"])
            )
            context["formulario"] = data_forms

    return render(request, "solicitudes_software.html", context)


def form_info1(request):
    context = {}
    if request.GET:
        if "id_user" in request.GET:
            data_forms = SoftwareForm.objects.get(
                id_request=int(request.GET["id_user"])
            )
            context["formulario"] = data_forms
    return render(request, "info_formulario1.html", context)


def form_list(request):
    software_forms = SoftwareForm.objects.all().order_by(
        "-creation_date", "-id_request"
    )
    data = {"solicitudes": software_forms}
    return render(request, "listado_formularios.html", data)


def form_info(request):
    software_forms = SoftwareForm.objects.all()
    data = {"solicitudes": software_forms}
    return render(request, "info_formulario.html", data)


def software_request_done(request):
    return render(request, "formulario_listo.html")


def prueba(request):
    form = SoftwareRequestForm()
    return render(request, "formulario_copy.html", {"form": form})


class SoftwareRequestView(HttpRequest):
    def form_create(request):
        form = SoftwareRequestForm()
        if request.method == "POST":
            form = SoftwareRequestForm(request.POST)
            if form.is_valid():
                form.save()
                form = SoftwareRequestForm()
            context = {"form": form}

        return render(request, "formulario_listo.html", context)


def search_form(request):
    search = request.GET["buscar"]
    software_forms = SoftwareForm.objects.filter(name_user__icontains=search)
    context = {"solicitudes": software_forms}
    # if search:
    #     licenses = LicensesList.objects.filter(
    #         Q(license_name__icontains = search),
    #         Q(license_type__icontains = search)
    #     ).distinct()

    return render(request, "listado_formularios.html", context)


def status_form(request, id):

    status = request.POST["status"]

    SoftwareForm.objects.filter(id_request=id).update(status=status)

    software_forms = SoftwareForm.objects.all()
    data = {"solicitudes": software_forms}

    return render(request, "listado_formularios.html", data)


# ------LICENCIAS------#


def adm_licencias(request):
    licenses_lista = LicensesList.objects.all()
    data = {"listado_de_licencias": licenses_lista}

    return render(request, "listado_licencias.html", data)


def enter_licenses(request):
    license_form = EnterLicensesForm()
    return render(request, "ingresar_licencia.html", {"license_form": license_form})


class EnterLicensesView(HttpRequest):
    def enter_license(request):
        license_form = EnterLicensesForm()
        if request.method == "POST":
            license_form = EnterLicensesForm(request.POST)
            if license_form.is_valid():
                license_form.save()
                license_form = EnterLicensesForm()
            context = {"license_form": license_form}

        return render(request, "licencia_lista.html", context)


def edit_license(request, id):

    license_form = get_object_or_404(LicensesList, id_license=id)

    data = {"license_form": EnterLicensesForm(instance=license_form)}

    data["info"] = id
    print(data)
    if request.method == "POST":
        form = EnterLicensesForm(data=request.POST, instance=license_form)
        if form.is_valid():
            form.save()
            return redirect(to="licenses:adm_licencias")
        data["license_form"] = form

    return render(request, "editar_licencia.html", data)


def delete_license(request, id):

    license_form = get_object_or_404(LicensesList, id_license=id)
    license_form.delete()
    return redirect(to="licenses:adm_licencias")


def search_license(request):
    search = request.GET["buscar"]
    listado_de_licencias = LicensesList.objects.filter(license_name__icontains=search)
    print(listado_de_licencias)
    context = {"listado_de_licencias": listado_de_licencias}
    # if search:
    #     licenses = LicensesList.objects.filter(
    #         Q(license_name__icontains = search),
    #         Q(license_type__icontains = search)
    #     ).distinct()

    return render(request, "listado_licencias.html", context)


# ------REPORTES------#


def reportes(request):
    context = {}
    # -----------Licencias-----------#
    all_licenses = LicensesList.objects.all()
    total_licenses = len(all_licenses)
    context["total_licenses"] = total_licenses
    today = datetime.now()
    this_year = today.year
    this_year_licenses = all_licenses.filter(creation_date__year=this_year)
    due_date = today + timedelta(weeks=8)
    licenses_near_due_date = all_licenses.filter(
        license_due_date__range=(today, due_date)
    )
    total_licenses_near_due_date = len(licenses_near_due_date)
    context["total_licenses_near_due_date"] = total_licenses_near_due_date
    nodelocked_licenses = len(this_year_licenses.filter(license_type=2))
    context["nodelocked_licenses"] = nodelocked_licenses
    float_licenses = len(this_year_licenses.filter(license_type=3))
    context["float_licenses"] = float_licenses
    fisica_licenses = len(this_year_licenses.filter(license_type=4))
    context["fisica_licenses"] = fisica_licenses

    # -----------Formularios-----------#
    all_forms_request = SoftwareForm.objects.all()
    this_year_requests = all_forms_request.filter(creation_date__year=this_year)

    total_forms_requested = len(this_year_requests)
    context["total_forms_requested"] = total_forms_requested
    total_forms_done = len(this_year_requests.filter(status=3))
    context["total_forms_done"] = total_forms_done
    total_forms_rejected = len(this_year_requests.filter(status=4))
    context["total_forms_rejected"] = total_forms_rejected

    context["yearly_software_request"] = {
        "January": len(this_year_requests.filter(creation_date__month=1)),
        "February": len(this_year_requests.filter(creation_date__month=2)),
        "March": len(this_year_requests.filter(creation_date__month=3)),
        "April": len(this_year_requests.filter(creation_date__month=4)),
        "May": len(this_year_requests.filter(creation_date__month=5)),
        "June": len(this_year_requests.filter(creation_date__month=6)),
        "July": len(this_year_requests.filter(creation_date__month=7)),
        "August": len(this_year_requests.filter(creation_date__month=8)),
        "September": len(this_year_requests.filter(creation_date__month=9)),
        "October": len(this_year_requests.filter(creation_date__month=10)),
        "November": len(this_year_requests.filter(creation_date__month=11)),
        "December": len(this_year_requests.filter(creation_date__month=12)),
    }
    context["yearly_software_done"] = {
        "January": len(this_year_requests.filter(creation_date__month=1, status=3)),
        "February": len(this_year_requests.filter(creation_date__month=2, status=3)),
        "March": len(this_year_requests.filter(creation_date__month=3, status=3)),
        "April": len(this_year_requests.filter(creation_date__month=4, status=3)),
        "May": len(this_year_requests.filter(creation_date__month=5, status=3)),
        "June": len(this_year_requests.filter(creation_date__month=6, status=3)),
        "July": len(this_year_requests.filter(creation_date__month=7, status=3)),
        "August": len(this_year_requests.filter(creation_date__month=8, status=3)),
        "September": len(this_year_requests.filter(creation_date__month=9, status=3)),
        "October": len(this_year_requests.filter(creation_date__month=10, status=3)),
        "November": len(this_year_requests.filter(creation_date__month=11, status=3)),
        "December": len(this_year_requests.filter(creation_date__month=12, status=3)),
    }
    context["yearly_software_rejected"] = {
        "January": len(this_year_requests.filter(creation_date__month=1, status=4)),
        "February": len(this_year_requests.filter(creation_date__month=2, status=4)),
        "March": len(this_year_requests.filter(creation_date__month=3, status=4)),
        "April": len(this_year_requests.filter(creation_date__month=4, status=4)),
        "May": len(this_year_requests.filter(creation_date__month=5, status=4)),
        "June": len(this_year_requests.filter(creation_date__month=6, status=4)),
        "July": len(this_year_requests.filter(creation_date__month=7, status=4)),
        "August": len(this_year_requests.filter(creation_date__month=8, status=4)),
        "September": len(this_year_requests.filter(creation_date__month=9, status=4)),
        "October": len(this_year_requests.filter(creation_date__month=10, status=4)),
        "November": len(this_year_requests.filter(creation_date__month=11, status=4)),
        "December": len(this_year_requests.filter(creation_date__month=12, status=4)),
    }

    return render(request, "reportes.html", context)


# ------EQUIPOS------#


def labs(request):
    return render(request, "visualizar_labs.html")


def equipos(request):
    return render(request, "visualizar_equipos.html")


def pc(request):
    return render(request, "pc.html")
