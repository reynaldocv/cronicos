from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from re import template

from datetime import date

from usuarios.views.reporters import *

from usuarios.models import Paciente
from usuarios.models import Hospital
















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
