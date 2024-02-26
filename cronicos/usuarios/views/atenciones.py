from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from re import template
from datetime import date, datetime
from django.urls import reverse

import calendar

from usuarios.models import Paciente
from usuarios.models import Hospital
from usuarios.models import Mosare
from usuarios.models import Pie
from usuarios.models import Ekg
from usuarios.models import Referencia
from usuarios.models import Atencion
from usuarios.models import Especialidad

from usuarios.modules import codeHtml

from usuarios.views.pacientes import *

meses = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]
Meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]

def isValidMesYear(_month, _year, minData):
    _minData = date(minData.year, minData.month, 1)
    data = date(_year, _month, 1)
    today = date.today()

    return _minData <= data < today

def resumenm(request):
    _pacientes = pacientes_full(True, None)

    thisMonth = date.today().month
    thisYear = date.today().year 
    
    prevMonth = thisMonth - 1
    prevYear = thisYear

    if prevMonth  == 0: 
        prevMonth = 12
        prevYear -= 1  

    for (i, paciente) in enumerate(_pacientes): 
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

        paciente.edad = codeHtml.html_edad(paciente.nacimiento, paciente.muerto, paciente.fechaMuerto, 0)

        paciente.hta = codeHtml.html_hipertension(paciente.hta, paciente.fechaHta)
        paciente.dm  = codeHtml.html_deabetes(paciente.dm, paciente.fechaDm)

    template = loader.get_template("_resumen.html")

           
    context = {
        "pacientes": _pacientes,
        "month": {"prev": meses[prevMonth], "now": meses[thisMonth], "nowInt": thisMonth},
        "year": {"prev": prevYear, "now": thisYear},
    }

    return HttpResponse(template.render(context, request))


def resumen(request):
    _pacientes = pacientes_full(True, None)

    thisMonth = date.today().month
    thisYear = date.today().year 
    
    prevMonth = thisMonth - 1
    prevYear = thisYear

    prevDotacion = Atencion.objects.filter(fecha__month = prevMonth, fecha__year = prevYear)
    lastDotacion = Atencion.objects.filter(fecha__month = thisMonth, fecha__year = thisYear)
    prevDot = {}
    lastDot = {}

    #pies = Pie.objects.raw("select * from Pie group by dni")

    for dotacion in prevDotacion: 
        prevDot[dotacion.dni.dni] = codeHtml.html_dotacion(dotacion)

    for dotacion in lastDotacion: 
        lastDot[dotacion.dni.dni] = codeHtml.html_dotacion(dotacion)

    for _paciente in _pacientes: 
        if _paciente.dni in lastDot: 
            _paciente.atencion = lastDot[_paciente.dni]
        
        if _paciente.dni in prevDot: 
            _paciente.prevAtencion = prevDot[_paciente.dni]    

        lastPies = Pie.objects.filter(dni = _paciente.dni).order_by("-data")
        lastEkgs = Ekg.objects.filter(dni = _paciente.dni).order_by("-data")
        lastMosares = Mosare.objects.filter(dni = _paciente.dni).order_by("-data")

        if len(lastPies) > 0: 
            _paciente.lastPie = codeHtml.html_pie(lastPies[0])

        if len(lastEkgs) > 0: 
            _paciente.lastEkg = codeHtml.html_ekg(lastEkgs[0])

        if len(lastMosares) > 0: 
            _paciente.lastMosare = codeHtml.html_mosare(lastMosares[0])

    #pies = Pie.objects.dis

    template = loader.get_template("_resumen.html")
           
    context = {
        "pacientes": _pacientes,        
        "month": {"prev": meses[prevMonth], "now": meses[thisMonth], "nowInt": thisMonth},
        "year": {"prev": prevYear, "now": thisYear},
        "pies":_pacientes,
        
    }

    return HttpResponse(template.render(context, request))



def atencion_kit(_dni, _thisYear):
    
    _paciente = paciente_full(_dni)

    _minData = date.today()

    if _paciente.hta: 
        _minData = min(_minData, _paciente.fechaHta)

    if _paciente.dm: 
        _minData = min(_minData, _paciente.fechaDm)

    _maxYear = date.today().year
    _minYear = _minData.year

    consultas = {}

    consultas["dotacion"] = []
    consultas["acto"] = []
    consultas["presion"] = []
    consultas["hemoglucotest"] = []
    consultas["peso"] = []
    consultas["talla"] = []
    consultas["perimetro"] = []
    consultas["morisky"] = []
    consultas["imc"] = []
    consultas["imcDescripcion"] = []
    consultas["status"] = []
    consultas["observacion"] = []
    consultas["edad"] = []
    consultas["status"] = []

    chequeos = {}
    chequeos["chequeo"] = []
    chequeos["status"] = []

    cardiogramas = {}
    cardiogramas["ekg"] = []
    cardiogramas["status"] = []

    mosares = Mosare.objects.filter(id = _dni  +"-"+ _thisYear)

    if len(mosares) > 0: 
        mosare = mosares[0]

    else: 
        mosare = {"seen": 0}

    referencias = Referencia.objects.filter(data__year = _thisYear, dni= _dni).order_by("-data")
    
    for mes in range(1, 13):
        _id = "-".join([_dni, str(mes), _thisYear])
        
        atenciones = Atencion.objects.filter(id = _id)

        if len(atenciones) > 0:        
            atencion = atenciones[0] 

            consultas["dotacion"].append(codeHtml.html_dotacion_icon(atencion))
            consultas["acto"].append(atencion.acto)
            consultas["presion"].append(atencion.presion)
            consultas["hemoglucotest"].append(atencion.hemotest)
            consultas["peso"].append(atencion.peso)
            consultas["talla"].append(atencion.talla)
            consultas["perimetro"].append(atencion.perimetro)
            consultas["morisky"].append(codeHtml.html_morisky(atencion.morisky))
            consultas["imc"].append(codeHtml.html_Imc(atencion.imc, atencion.edad))
            consultas["imcDescripcion"].append(atencion.imcDescripcion)
            consultas["observacion"].append(atencion.observacion)            
            consultas["status"].append({"status": 2, "month": mes})

        else:             
            for key in consultas: 
                consultas[key].append("")

            if isValidMesYear(mes, int(_thisYear), _minData):
                consultas["status"][-1]= {"status": 1, "month": mes}

            else: 
                consultas["status"][-1] = {"status": 0, "month": mes}


        pies = Pie.objects.filter(id = _id).order_by("-data")

        if len(pies) > 0: 
            chequeos["chequeo"].append(codeHtml.html_chequeo_icon(pies[0]))
            chequeos["status"].append({"status": 2, "month": mes})

        else: 
            chequeos["chequeo"].append("{}")

            if isValidMesYear(mes, int(_thisYear), _paciente.fechaDm):
                chequeos["status"].append({"status": 1, "month": mes})

            else: 
                chequeos["status"].append({"status": 0, "month": mes})

        ekgs = Ekg.objects.filter(id = _id).order_by("-data")

        if len(ekgs) > 0: 
            
            cardiogramas["ekg"].append(codeHtml.html_cardiograma_icon(ekgs[0]))
            cardiogramas["status"].append({"status": 2, "month": mes})

        else: 
            cardiogramas["ekg"].append("")

            if isValidMesYear(mes, int(_thisYear), _paciente.fechaHta):
                cardiogramas["status"].append({"status": 1, "month": mes})

            else: 
                cardiogramas["status"].append({"status": 0, "month": mes})

    _minimum = date(int(_thisYear), 1, 1)
    _maximum = date(int(_thisYear), 12, 31)

    _especialidades = Especialidad.objects.all()
    _hospital = Hospital.objects.filter(id = 0)[0]
    
    context = {        
        "paciente": _paciente,       
        "consultas": consultas,
        "pies": chequeos, 
        "ekgs": cardiogramas, 
        "mosare": mosare, 
        "refs": referencias, 
        
        "especialidades": _especialidades, 
        "hospital" : _hospital,
        "years": {"min": _minYear, "max": _maxYear, "now": _thisYear },
        "days": {"first": _minimum, "last": _maximum},
        "meses": [{"int": i, "nombre": meses[i]} for i in range(1, 13)],
    }

    return context


















































def dotacion_new(request):
    _dni = request.POST["nowDni"]

    _thisMonth = int(request.POST["nowMonth"])
    _thisYear = int(request.POST["nowYear"])

    _prevMonth = _thisMonth - 1 
    _prevYear = _thisYear

    if _prevMonth == 0: 
        _prevMonth = 12 
        _prevYear -= 1 

    (_, last) = calendar.monthrange(_thisYear, _thisMonth)

    _minimum = date(_thisYear, _thisMonth, 1)
    _maximum = date(_thisYear, _thisMonth, last)
    
    mypaciente = paciente_full(_dni)
    mypaciente.edadAtencion = codeHtml.ageInYears(_maximum, mypaciente.nacimiento)

    _id = "-".join([_dni, str(_prevMonth), str(_prevYear)])

    prevAtencion = Atencion.objects.filter(id = _id)

    if len(prevAtencion) > 0: 
        prevAtencion = prevAtencion[0]
        prevAtencion.dotacion = codeHtml.html_selected_dotacion(prevAtencion.dotacion)
        prevAtencion.morisky = codeHtml.html_selected_morisky(prevAtencion.morisky)

    else: 
        prevAtencion = {"dotacion": codeHtml.html_selected_dotacion("")}


    template = loader.get_template("dotacion_new.html")

    context = {
        "paciente": mypaciente,
        "prevAtencion": prevAtencion,
        "prevMonth": {"int" : _prevMonth, "name": Meses[_prevMonth]},
        "thisMonth": {"int" : _thisMonth, "name": Meses[_thisMonth]},
        "years": {"prev": _prevYear, "now": _thisYear},
        "datas" : {"minimumData": _minimum, "maximumData": _maximum},
        "thisDni": _dni,
    }

    return HttpResponse(template.render(context, request))

def dotacion_add(request):
    atencion = Atencion()

    _dni = request.POST["nowDni"]
    _thisMonth = request.POST["nowMonth"]
    _thisYear = request.POST["nowYear"]

    if _dni and _thisMonth and _thisYear:
        _id = "-".join([_dni, _thisMonth, _thisYear])

        atencion.id = _id
        atencion.dni = Paciente.objects.filter(dni = _dni)[0]
        atencion.dotacion = request.POST["nowDotacion"]        
        atencion.fecha = request.POST["nowData"]
        atencion.acto = request.POST["nowActo"]
        atencion.presion = request.POST["nowPresion"]
        atencion.hemotest = request.POST["nowHemotest"]
        atencion.peso = request.POST["nowPeso"]
        atencion.talla = request.POST["nowTalla"]
        atencion.imc = request.POST["nowImc"]
        atencion.imcDescripcion = request.POST["nowImcDescripcion"]
        atencion.perimetro = request.POST["nowPerimetro"]
        atencion.morisky = request.POST["nowMorisky"]

        tmp = datetime.strptime(request.POST["nowData"], '%Y-%m-%d').date()

        atencion.edad = str(codeHtml.ageInYears(tmp, atencion.dni.nacimiento))

        if atencion.talla and atencion.peso: 
            atencion.imc = float(atencion.peso)/((float(atencion.talla))**2)

        atencion.observacion = request.POST["nowObservacion"]

        atencion.save()        

        return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _thisYear,"dot" )))
    

def dotacion_mod(request):
    _dni = request.POST["nowDni"]

    _thisMonth = int(request.POST["nowMonth"])
    _thisYear = int(request.POST["nowYear"])

    (_, last) = calendar.monthrange(_thisYear, _thisMonth)

    _minimum = date(_thisYear, _thisMonth, 1)
    _maximum = date(_thisYear, _thisMonth, last)
    
    mypaciente = paciente_full(_dni)

    _id = "-".join([_dni, str(_thisMonth), str(_thisYear)])

    prevAtencion = Atencion.objects.filter(id = _id)

    if len(prevAtencion) > 0: 
        prevAtencion = prevAtencion[0]
        prevAtencion.dotacion = codeHtml.html_selected_dotacion(prevAtencion.dotacion)
        prevAtencion.morisky = codeHtml.html_selected_morisky(prevAtencion.morisky)

    else: 
        prevAtencion = {"dotacion": codeHtml.html_selected_dotacion("")}


    template = loader.get_template("dotacion_mod.html")

    context = {
        "paciente": mypaciente,
        "prevMonth": _thisMonth, 
        "prevMonthNombre": Meses[_thisMonth],
        "prevYear": _thisYear, 
        "thisMonth": _thisMonth, 
        "thisMonthNombre":Meses[_thisMonth], 
        "thisYear": _thisYear,
        "minimumData": _minimum, 
        "maximumData": _maximum,
        "dni": _dni,
        "prevAtencion": prevAtencion,
    
    }

    return HttpResponse(template.render(context, request))


def dotacion_alter(request):
    atencion = Atencion()

    _dni = request.POST["nowDni"]
    _thisMonth = request.POST["nowMonth"]
    _thisYear = request.POST["nowYear"]

    if _dni and _thisMonth and _thisYear:
        _id = "-".join([_dni, _thisMonth, _thisYear])

        atencion = Atencion.objects.filter(id = _id)[0]

        atencion.dotacion = request.POST["nowDotacion"]        
        atencion.fecha = request.POST["nowData"]
        atencion.acto = request.POST["nowActo"]
        atencion.presion = request.POST["nowPresion"]
        atencion.hemotest = request.POST["nowHemotest"]
        atencion.peso = request.POST["nowPeso"]
        atencion.talla = request.POST["nowTalla"]
        atencion.imc = request.POST["nowImc"]
        atencion.imcDescripcion = request.POST["nowImcDescripcion"]
        atencion.perimetro = request.POST["nowPerimetro"]
        atencion.morisky = request.POST["nowMorisky"]

        tmp = datetime.strptime(request.POST["nowData"], '%Y-%m-%d').date()

        atencion.edad = str(codeHtml.ageInYears(tmp, atencion.dni.nacimiento))

        if atencion.talla and atencion.peso: 
            atencion.imc = float(atencion.peso)/((float(atencion.talla)**2))

        atencion.observacion = request.POST["nowObservacion"]

        atencion.save()

        
        return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _thisYear,"dot" )))

















































def ekg_new(request):
    _dni = request.POST["nowDni"]
    _mes = int(request.POST["nowMonth"])
    _year = int(request.POST["nowYear"])
        
    _paciente = paciente_full(_dni)
    
    (_, last) = calendar.monthrange(_year, _mes)

    _minimum = date(_year, _mes, 1)
    _maximum = date(_year, _mes, last)

    template = loader.get_template("ekg_new.html")

    context = {
        "nowDni": _dni, 
        "nowMonth": _mes,
        "nowYear": _year,
        "paciente": _paciente, 
        "minimumData" : _minimum, 
        "maximumData" : _maximum,  
        "years": {"now": _year},              
    }

    return HttpResponse(template.render(context, request))

def ekg_add(request):
    _dni = request.POST["nowDni"]
    _mes = request.POST["nowMonth"]
    _thisYear = request.POST["nowYear"]
    
    _id = "-".join([_dni, _mes, _thisYear])

    ekg = Ekg()

    ekg.id = _id
    ekg.data = request.POST["nowData"] 
    ekg.dni = Paciente.objects.filter(dni = _dni)[0]
    ekg.esNormal = request.POST["nowNormal"]
    ekg.observacion = request.POST["nowObservacion"]

    ekg.save()

    return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _thisYear,"ekg" )))

def ekg_alter(request):
    _dni = request.POST["nowDni"]
    _mes = request.POST["nowMonth"]
    _thisYear = request.POST["nowYear"]

    _id = "-".join([_dni, _mes, _thisYear])

    ekg = Ekg.objects.filter(id = _id)[0]

    ekg.data = request.POST["nowData"] 
    ekg.esNormal = request.POST["nowNormal"]
    ekg.observacion = request.POST["nowObservacion"]

    ekg.save()

    return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _thisYear,"ekg" )))

def ekg_mod(request):
    _dni = request.POST["nowDni"]
    _mes = request.POST["nowMonth"]
    _year = request.POST["nowYear"]   

    mypaciente = paciente_full(_dni)

    _id = "-".join([_dni, _mes, _year])

    ekg= Ekg.objects.filter(id = _id)[0]

    (_, last) = calendar.monthrange(int(_year), int(_mes))

    _minimum = date(int(_year), int(_mes), 1)
    _maximum = date(int(_year), int(_mes), last)
    
    context = {
        "nowDni": _dni, 
        "nowMonth": _mes,
        "nowYear": _year,
        "paciente": mypaciente, 
        "minimumData" : _minimum, 
        "maximumData" : _maximum, 
        "ekg" : ekg,                
    }

    template = loader.get_template("ekg_mod.html")
    
    return HttpResponse(template.render(context, request))












































def pie_new(request):
    _dni = request.POST["nowDni"]
    _mes = int(request.POST["nowMonth"])
    _year = int(request.POST["nowYear"])
        
    mypaciente = paciente_full(_dni)

    template = loader.get_template("pie_new.html")
    
    (_, last) = calendar.monthrange(_year, _mes)

    _minimum = date(_year, _mes, 1)
    _maximum = date(_year, _mes, last)

    context = {
        "nowDni": _dni, 
        "nowMonth": _mes,
        "nowYear": _year,
        "paciente": mypaciente, 
        "minimumData" : _minimum, 
        "maximumData" : _maximum,                
    }

    return HttpResponse(template.render(context, request))

def pie_add(request):
    _dni = request.POST["nowDni"]
    _mes = request.POST["nowMonth"]
    _thisYear = request.POST["nowYear"]

    _id = "-".join([_dni, _mes, _thisYear])

    pie = Pie()

    pie.id = _id
    pie.data = request.POST["nowData"] 
    pie.dni = Paciente.objects.filter(dni = _dni)[0]
    pie.conLesion = request.POST["nowLesion"]
    pie.observacion = request.POST["nowObservacion"]

    pie.save() 

    return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _thisYear,"pie" )))


def pie_alter(request):
    _dni = request.POST["nowDni"]
    _mes = request.POST["nowMonth"]
    _thisYear = request.POST["nowYear"]

    _id = "-".join([_dni, _mes, _thisYear])

    pie = Pie.objects.filter(id = _id)[0]

    pie.data = request.POST["nowData"] 
    pie.conLesion = request.POST["nowLesion"]
    pie.observacion = request.POST["nowObservacion"]

    pie.save()

    return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _thisYear,"pie" )))


def pie_mod(request):
    _dni = request.POST["nowDni"]
    _mes = request.POST["nowMonth"]
    _year = request.POST["nowYear"]   

    mypaciente = paciente_full(_dni)

    _id = "-".join([_dni, _mes, _year])

    pie = Pie.objects.filter(id = _id)[0]

    (_, last) = calendar.monthrange(int(_year), int(_mes))

    _minimum = date(int(_year), int(_mes), 1)
    _maximum = date(int(_year), int(_mes), last)
    
    context = {
        "nowDni": _dni, 
        "nowMonth": _mes,
        "nowYear": _year,
        "paciente": mypaciente, 
        "minimumData" : _minimum, 
        "maximumData" : _maximum, 
        "pie" : pie,                
    }

    template = loader.get_template("pie_mod.html")
    
    return HttpResponse(template.render(context, request))




















































def mosare_add(request):
    _dni = request.POST["nowDni"]      
    _thisYear = request.POST["nowYear"]

    _id = "-".join([_dni, _thisYear])

    mosares = Mosare.objects.filter(id = _id)

    if len(mosares) > 0: 
        mosare = mosares[0]
    
    else: 
        mosare = Mosare()    
        mosare.id = _id

    mosare.data = request.POST["nowData"] 
    mosare.dni = Paciente.objects.filter(dni = _dni)[0]

    mosare.creatinina = request.POST["nowCreatinina"] 
    mosare.tfge = request.POST["nowTfge"]
    mosare.albuminuria = request.POST["nowAlbuminuria"]
    mosare.creatinuria = request.POST["nowCreatinuria"]
    mosare.tasa = request.POST["nowTasa"]
    mosare.tasaDescripcion = request.POST["nowDescripcion"]

    mosare.save()

    return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _thisYear,"msr" )))

    



































def referencia_add(request):
    _dni = request.POST["nowDni"]      
    _year = request.POST["nowYear"]

    referencia = Referencia()

    referencia.data = request.POST["nowData"] 
    referencia.dni = Paciente.objects.filter(dni = _dni)[0]

    referencia.observacion = request.POST["nowObservacion"] 
    referencia.especialidad = Especialidad.objects.filter(id = request.POST["nowEspecialidad"])[0]
    
    referencia.save()
    
    return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _year,"ref" )))


def referencia_alter(request):
    _id = request.POST["nowId"]  

    _dni = request.POST["nowDni"]
    _year = request.POST["nowYear"]

    referencia = Referencia.objects.filter(id = _id)[0]

    referencia.data = request.POST["nowData"] 
    referencia.observacion = request.POST["nowObservacion"]
    referencia.atendido = request.POST["nowAtendido"]
    referencia.especialidad = Especialidad.objects.filter(id = request.POST["nowEspecialidad"])[0]
    
    referencia.save()

    return HttpResponseRedirect(reverse("pacienteOption", args = (_dni, _year,"ref" )))

def referencia_mod(request):
    _id = request.POST["nowId"]
    _dni = request.POST["nowDni"]  
    _year = request.POST["nowYear"]   

    mypaciente = paciente_full(_dni)

    referencia = Referencia.objects.filter(id = _id)[0]

    especialidades = Especialidad.objects.all()

    _minimum = date(int(_year), 1, 1)
    _maximum = date(int(_year), 12, 31)
    
    context = {
        "thisDni": _dni,         
        "nowYear": _year,
        "paciente": mypaciente, 
        "days": {"first": _minimum, "last": _maximum},
        "referencia" : referencia, 
        "especialidades": especialidades,         
        "years": {"now": _year },      
    }

    template = loader.get_template("referencia_mod.html")
    
    return HttpResponse(template.render(context, request))















































def pacienteDniYear(request, _dni, _year):
    context = atencion_kit(_dni, _year)

    return render(request, "atenciones.html", context)

def pacienteOption(request, _dni, _year, _option):
    context = atencion_kit(_dni, _year)

    context["option"] = _option

    return render(request, "atenciones.html", context)
































    


