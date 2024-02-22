from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from re import template
from datetime import date

from usuarios.models import Paciente
from usuarios.models import Hospital
from usuarios.modules import codeHtml

meses = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]
Meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]


def paciente_full(_dni):

    _paciente = Paciente.objects.filter(dni = _dni)[0]

    _paciente.edad = codeHtml.html_edad(_paciente.nacimiento, _paciente.muerto, _paciente.fechaMuerto, 0)
    _paciente.hipertension = codeHtml.html_hipertension(_paciente.hta, _paciente.fechaHta)
    _paciente.deabetes  = codeHtml.html_deabetes(_paciente.dm, _paciente.fechaDm)
    _paciente.deceso = codeHtml.html_muerto(_paciente.muerto, _paciente.fechaMuerto)

    return _paciente

def pacientes_full(_vivo, _year):
    if _vivo: 
        _pacientes = Paciente.objects.filter(muerto = False).order_by("nombre")    
    
    else:
        _pacientes = Paciente.objects.filter(muerto = 1, fechaMuerto__year = _year).order_by("nombre")    
    
    for _paciente in _pacientes:         
        _paciente.edad = codeHtml.html_edad(_paciente.nacimiento, _paciente.muerto, _paciente.fechaMuerto, 0)
        _paciente.hipertension = codeHtml.html_hipertension(_paciente.hta, _paciente.fechaHta)
        _paciente.deabetes = codeHtml.html_deabetes(_paciente.dm, _paciente.fechaDm)
        _paciente.deceso = codeHtml.html_dead(_paciente.muerto, _paciente.fechaMuerto) 
    
    return _pacientes


def paciente_new(request):
    _pacientes = Paciente.objects.all().values()
    _hospitales = Hospital.objects.all().values()
    _hospital = Hospital.objects.filter(id = 0)[0]

    _template = loader.get_template("paciente_new.html")

    _context = {
        "hospital": _hospital,
        "fecha": date.today(),
        "pacientes": _pacientes,
        "hospitales": _hospitales,
    }

    return HttpResponse(_template.render(_context, request))


def paciente_add(request):
    _dni = request.POST["myDNI"]
    _idHospital = request.POST["myCentro"]

    _pacientes = Paciente.objects.filter(dni = _dni)
    _hospitales = Hospital.objects.filter(id = _idHospital)

    if len(_pacientes) == 0:
        paciente = Paciente()

        paciente.dni = _dni
        paciente.nombre = request.POST["myNombre"].upper()
        paciente.direccion = request.POST["myDireccion"].title()
        paciente.hospital = _hospitales[0]
        paciente.historia = request.POST["myHistoria"]
        paciente.celular = request.POST["myCelular"]
        paciente.sexo = request.POST["mySexo"]

        if request.POST.get("myNacimiento"):
            paciente.nacimiento = request.POST["myNacimiento"]

        paciente.observacion = request.POST["myObservacion"]

        paciente.status = 1
        paciente.muerto = 0        

        if request.POST.get("myHTA"):
            paciente.hta = request.POST["myHTA"]
            paciente.fechaHta = request.POST["myHTAdata"]
        if request.POST.get("myDM"):
            paciente.dm = request.POST["myDM"]
            paciente.fechaDm  = request.POST["myDMdata"]

        paciente.observacion = request.POST["myObservacion"]
        
        paciente.save()

    return pacienteDni(request, _dni)
 
def paciente_mod(request):
    _dni = request.POST["nowDni"]
    _paciente = paciente_full(_dni)
    _hospitales = Hospital.objects.all().values()
    

    template = loader.get_template("paciente_mod.html")

    context = {
        "paciente": _paciente,
        "hospitales": _hospitales,
    }

    return HttpResponse(template.render(context, request))


def paciente_alter(request):
    _dni = request.POST["myDNI"]
    _hospitales = Hospital.objects.filter(id = request.POST["myCentro"])

    _pacientes = Paciente.objects.filter(dni = _dni)

    if len(_pacientes) > 0:
        _paciente = _pacientes[0]

        _paciente.dni = _dni
        _paciente.nombre = request.POST["myNombre"].upper()
        _paciente.direccion = request.POST["myDireccion"].title()
        _paciente.hospital = _hospitales[0]
        _paciente.historia = request.POST["myHistoria"]
        _paciente.celular = request.POST["myCelular"]
        _paciente.sexo = request.POST["mySexo"]
        _paciente.nacimiento = request.POST["myNacimiento"]

        _paciente.status = 1
        _paciente.muerto = 0
        
        if request.POST.get("myHTA"):
            _paciente.hta = request.POST["myHTA"]

            if request.POST["myHTAdata"] != "":
                _paciente.fechaHta = request.POST["myHTAdata"]
        else: 
            _paciente.hta = 0        

        if request.POST.get("myDM"):
            _paciente.dm = request.POST["myDM"]
            
            if request.POST["myDMdata"] != "":                 
                _paciente.fechaDm= request.POST["myDMdata"]

        else: 
            _paciente.deabetes = 0
        
        _paciente.observacion = request.POST["myObservacion"]

        _paciente.save()

    return pacienteDni(request, _dni)
        
def paciente_kill(request):
    _dni = request.POST["nowDni"]

    _paciente = paciente_full(_dni)

    if "action" in request.POST: 
        fecha = request.POST["nowData"]
        _observación = request.POST["nowObservacion"]

        _paciente.muerto = True
        _paciente.fechaMuerto = fecha
        _paciente.observacionMuerto = _observación

        _paciente.save() 

        return pacienteDni(request, _dni)

    else:        
        template = loader.get_template("paciente_kill.html")

        _hospitales = Hospital.objects.all().values()

        context = {
            "paciente": _paciente,
            "hospitales": _hospitales,
        }

        return HttpResponse(template.render(context, request))


def resumen(request):
    mypacientes = Paciente.objects.filter(muerto = 0).order_by("nombre")

    thisMonth = date.today().month
    thisYear = date.today().year 
    
    prevMonth = thisMonth - 1
    prevYear = thisYear

    if prevMonth  == 0: 
        prevMonth = 12
        prevYear -= 1  

    for (i, paciente) in enumerate(mypacientes): 
        _dni = paciente.dni

        _id = "-".join([_dni, str(thisMonth), str(thisYear)])

        # atención del último mes
        
        atencion = Atencion.objects.filter(id = _id)

        if len(atencion) > 0: 
            paciente.atencion = codeHtml.html_dotacion(atencion[0])

        _id = "-".join([_dni, str(prevMonth), str(thisYear)])

        # atención del penúltimo mes

        atencion = Atencion.objects.filter(id = _id)

        if len(atencion) > 0: 
            paciente.prevAtencion = codeHtml.html_dotacion(atencion[0])

        mosares = Mosare.objects.filter(dni = _dni).order_by("-data")

        if len(mosares) > 0: 
            paciente.mosare = codeHtml.html_mosare(mosares[0])
        else: 
            paciente.mosare = codeHtml.html_mosare(None)

        pies = Pie.objects.filter(dni = _dni).order_by("-data")

        if len(pies) > 0: 
            paciente.pie = codeHtml.html_pie(pies[0])
        else: 
            paciente.pie = codeHtml.html_pie(None)

        ekgs = Ekg.objects.filter(dni = _dni).order_by("-data")

        if len(ekgs) > 0: 
            paciente.ekg = codeHtml.html_cardiograma(ekgs[0])
        else: 
            paciente.ekg = codeHtml.html_cardiograma(None)

        paciente.edad = codeHtml.html_edad(paciente.nacimiento, paciente.estaMuerto, paciente.fechaMuerto, 0)

        paciente.hta = codeHtml.html_hipertension(paciente.hipertension, paciente.fechaHipertension)
        paciente.dm  = codeHtml.html_deabetes(paciente.deabetes, paciente.fechaDeabetes)

    template = loader.get_template("resumen.html")

           
    context = {
        "mypacientes": mypacientes,
        "prevMonth": prevMonth, 
        "month": {"prev": meses[prevMonth], "now": thisMonth, "nowInt": thisMonth},
        "year": {"prev": prevYear, "now": thisYear},
    }

    return HttpResponse(template.render(context, request))

def pacientes_list(request):
    _pacientes = pacientes_full(True, None)

    template = loader.get_template("pacientes_list.html")

    context = {
        "pacientes": _pacientes,
        "years": {"now": date.today().year},
    }
    return HttpResponse(template.render(context, request))

def muertos_list(request):
    if "nowYear" in request.POST:
        _thisYear = request.POST["nowYear"]

    else: 
        _thisYear = date.today().year

    _pacientes = pacientes_full(False, _thisYear)

    template = loader.get_template("muertos_list.html")

    context = {
        "pacientes": _pacientes,
        "years": {"now": _thisYear},
    }

    return HttpResponse(template.render(context, request))
    
def muerto_mod(request):
    _dni = request.POST["nowDni"]

    _paciente = paciente_full(_dni)
    _hospital = Hospital.objects.filter(id = "0")[0]

    template = loader.get_template("muerto_mod.html")
    
    context = {
        "hospital": _hospital,
        "paciente": _paciente,
        
    }
    return HttpResponse(template.render(context, request))

def muerto_alter(request):
    _dni = request.POST["nowDni"]
    
    paciente = Paciente.objects.filter(dni = _dni)[0]

    paciente.fechaMuerto = request.POST["nowFechaMuerto"]        
    paciente.observacionMuerto = request.POST["nowObservacionMuerto"]        

    paciente.save()

    return pacienteDni(request, _dni)















































def pacienteDni(request, _dni):
    if "nowYear" in request.POST: 
        _year = request.POST["nowYear"]

        return HttpResponseRedirect(reverse("pacienteDniYear", args = (_dni, _year)))
    
    else: 
        _year = str(date.today().year)
        _paciente = paciente_full(_dni)
        _hospitales = Hospital.objects.all().values()
    

        context = {
            "paciente": _paciente,              
            "hospitales" :_hospitales, 
        }

        return render(request, "paciente.html", context)

   












