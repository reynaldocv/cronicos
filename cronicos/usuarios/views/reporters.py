from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from re import template

from datetime import date

from usuarios.views.reporters import *


from usuarios.models import Atencion
from usuarios.models import Paciente
from usuarios.models import Hospital
from usuarios.models import Pie
from usuarios.models import Ekg

meses = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]
Meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]


def reporte_01(request):
    _Mhta_count = len(Paciente.objects.filter(muerto = 0, hta = True, dm = False, sexo = True))
    _Fhta_count = len(Paciente.objects.filter(muerto = 0, hta = True, dm = False, sexo = False))
    _Mdm_count = len(Paciente.objects.filter(muerto = 0, hta = False, dm = True, sexo = True))
    _Fdm_count = len(Paciente.objects.filter(muerto = 0, hta = False, dm = True, sexo = False))
    _MhtaDm_count = len(Paciente.objects.filter(muerto = 0, hta = True, dm = True, sexo = True))
    _FhtaDm_count = len(Paciente.objects.filter(muerto = 0, hta = True, dm = True, sexo = False))

    _total = len(Paciente.objects.filter(muerto = 0))
    _totalSum = _Mhta_count + _Fhta_count + _Mdm_count + _Fdm_count +  _MhtaDm_count +  _FhtaDm_count

    _context = {"usuarios": {"hombres": {"dm": _Mdm_count, "hta": _Mhta_count, "htaDm": _MhtaDm_count}, 
                            "mujeres": {"dm": _Fdm_count, "hta": _Fhta_count, "htaDm": _FhtaDm_count}, }, 
               "total" : {"hta": _Mhta_count + _Fhta_count, 
                          "dm" : _Mdm_count + _Fdm_count, 
                          "htaDm": _MhtaDm_count + _FhtaDm_count,
                          "suma": _totalSum, "database": _total}, 
               }

    _template = loader.get_template("reporte_01.html")

    return HttpResponse(_template.render(_context, request))


def reporte_pie(request):
    _year = date.today().year

    if "nowYear" in request.POST:
        _year = request.POST["nowYear"]

    _context = {}
    _total = len(Pie.objects.filter(data__year = _year))
       
    _context["conLesion"] = []
    _context["sinLesion"] = []
    _context["totalmes"] = []

    _totalconLesion = 0
    _totalsinLesion = 0

    for mes in range(1, 13):
        _conLesion = len(Pie.objects.filter(data__month = mes, data__year = _year, conLesion = True ))
        _sinLesion = len(Pie.objects.filter(data__month = mes, data__year = _year, conLesion = False ))

        _totalconLesion += _conLesion
        _totalsinLesion += _sinLesion

        _context["conLesion"].append(_conLesion) 
        _context["sinLesion"].append(_sinLesion) 
        _context["totalmes"].append(_conLesion + _sinLesion) 
    
    _context["conLesion"].append(_totalconLesion)
    _context["sinLesion"].append(_totalsinLesion)

    _context["total"] = _total
    _context["totalmes"].append(_totalconLesion + _totalsinLesion) 
    _context["years"] = {"now": _year}
    _context["meses"] = [meses[i] for i in range(1, 13)] + ["total"]

    _template = loader.get_template("reporte_pie.html")

    return HttpResponse(_template.render(_context, request))


def reporte_ekg(request):
    _year = date.today().year

    if "nowYear" in request.POST:
        _year = request.POST["nowYear"]

    _context = {}
    _total = len(Ekg.objects.filter(data__year = _year))
       
    _context["normal"] = []
    _context["alterado"] = []
    _context["totalmes"] = []

    _totalNormal = 0
    _totalAlterado = 0

    for mes in range(1, 13):
        _normal = len(Ekg.objects.filter(data__month = mes, data__year = _year, esNormal = True ))
        _alterado = len(Ekg.objects.filter(data__month = mes, data__year = _year, esNormal = False ))

        _totalNormal += _normal
        _totalAlterado += _alterado

        _context["normal"].append(_normal) 
        _context["alterado"].append(_alterado) 
        _context["totalmes"].append(_normal + _alterado) 
    
    _context["normal"].append(_totalNormal)
    _context["alterado"].append(_totalAlterado)

    _context["total"] = _total
    _context["totalmes"].append(_totalNormal + _totalAlterado) 
    _context["years"] = {"now": _year}
    _context["meses"] = [meses[i] for i in range(1, 13)] + ["total"]

    _template = loader.get_template("reporte_ekg.html")

    return HttpResponse(_template.render(_context, request))



def reporte_dot(request):
    _year = date.today().year

    if "nowYear" in request.POST:
        _year = request.POST["nowYear"]

    _context = {}
    _total = len(Atencion.objects.filter(fecha__year = _year))
       
    _context["dotacion1"] = []
    _context["dotacion2"] = []
    _context["dotacion3"] = []
    _context["dotacion0"] = []
    _context["totalmes"] = []

    _totalDotacion = [0, 0, 0, 0]
    
    for mes in range(1, 13):
        _dot0 = len(Atencion.objects.filter(fecha__month = mes, fecha__year = _year, dotacion = 0 ))
        _dot1 = len(Atencion.objects.filter(fecha__month = mes, fecha__year = _year, dotacion = 1 ))
        _dot2 = len(Atencion.objects.filter(fecha__month = mes, fecha__year = _year, dotacion = 2 ))
        _dot3 = len(Atencion.objects.filter(fecha__month = mes, fecha__year = _year, dotacion = 3 ))

        _totalDotacion[0] += _dot0
        _totalDotacion[1] += _dot1
        _totalDotacion[2] += _dot2        
        _totalDotacion[3] += _dot3
        
        _context["dotacion0"].append(_dot0) 
        _context["dotacion1"].append(_dot1) 
        _context["dotacion2"].append(_dot2) 
        _context["dotacion3"].append(_dot3) 

        _context["totalmes"].append(_dot0 + _dot1 + _dot2 + _dot3)
     
    _context["dotacion0"].append(_totalDotacion[0]) 
    _context["dotacion1"].append(_totalDotacion[1])
    _context["dotacion2"].append(_totalDotacion[2])
    _context["dotacion3"].append(_totalDotacion[3])

    _context["total"] = _total
    _context["totalmes"].append(sum(_totalDotacion)) 
    _context["years"] = {"now": _year}
    _context["meses"] = [meses[i] for i in range(1, 13)] + ["total"]

    _template = loader.get_template("reporte_dot.html")

    return HttpResponse(_template.render(_context, request))







    

    

    
    



    

































































def super_admin(request):
    if "texto" in request.POST:
        text = request.POST["texto"]

        lines = text.splitlines()

        for line in lines: 
            if line: 
                parts = line.split("#")

                pacientes = Paciente.objects.filter(dni = parts[0])

                if len(pacientes) > 0: 
                    paciente = pacientes[0]

                else:
                    paciente = Paciente()

                    paciente.dni = parts[0]

                paciente.nombre = parts[1]

                paciente.sexo = 1 if parts[2] == "M" else 0 

                edad = int(parts[3]) if parts[3].isdigit() else 0 

                paciente.nacimiento = date(date.today().year - edad, 1, 1)
                
                paciente.hospital = Hospital.objects.filter(id = 0)[0]

                paciente.historia = parts[6]
                paciente.direccion = parts[7].capitalize()
                
                paciente.hta = True
                paciente.dm = True
                paciente.fechaHta = date(2021, 1, 1)
                paciente.fechaDm = date(2021, 1, 1)

                paciente.celular = parts[8]

                paciente.save()

        context = {"texto": text}
    else: 
        context = {}

    
    return render(request, "_admin.html", context)
