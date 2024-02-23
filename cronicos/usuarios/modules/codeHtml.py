
from datetime import date, datetime, timedelta

meses = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]
Meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]

def html_dotacion(atencion):       
    day = str(atencion.fecha.day)
    num = atencion.dotacion
    
    if num == "0": 
        return '<span class="w3-tag w3-sand"><i class="fa fa-exchange"></i> / '+ day + '</span>'
    
    elif num == "1":
        return '<i style="color:lightblue" class="fa fa-user-doctor"></i><span class="w3-tag w3-pale-blue">  I - ' + day + '</span>'
    
    elif num == "2": 
        return '<i style="color:lightblue" class="fa fa-tablets"></i><span class="w3-tag w3-pale-blue"> II - ' + day + '</span>'
    
    else: 
        return '<i style="color:lightblue" class="fa fa-capsules"></i><span class="w3-tag w3-pale-blue"> III - ' + day + '</span>'

def html_dotacion_icon(atencion):    
    ans = {}
    day = str(atencion.fecha.day)

    if atencion.dotacion == "0": 
        ans["icon"] = '<i style="color:lightgray" class="fa fa-exchange"></i>'

    elif atencion.dotacion == "1": 
        ans["icon"] = '<i style="color:lightblue" class="fa fa-user-doctor"></i>'
    
    elif atencion.dotacion == "2": 
        ans["icon"] = '<i style="color:lightblue" class="fa fa-tablets"></i>'
    
    else: 
        ans["icon"] = '<i style="color:lightblue" class="fa fa-capsules"></i>'

    if atencion.dotacion == "0": 
        ans["day"] = '<span class="w3-tag w3-pale-blue"> ' + day + '</span>'

    elif atencion.dotacion == "1": 
        ans["day"] = '<span class="w3-tag w3-pale-blue">  I - ' + day + '</span>'
    
    elif atencion.dotacion == "2": 
        ans["day"] = '<span class="w3-tag w3-pale-blue">  II - ' + day + '</span>'
    
    else: 
        ans["day"] = '<span class="w3-tag w3-pale-blue">  III - ' + day + '</span>'

    ans["observacion"] = "[Dotación : " 
    ans["observacion"] += str(atencion.fecha.day) + " "
    ans["observacion"] += meses[atencion.fecha.month] + " "
    ans["observacion"] += str(atencion.fecha.year) + " ]"
    
    ans["observacion"] += " " + atencion.observacion
 
    return ans 


    
    num = atencion.dotacion
    
    if num == "0": 
        return '</i> / '+ day + '</span>'
    
    elif num == "1":
        return '<span class="w3-tag w3-pale-blue">  I - ' + day + '</span>'
    
    elif num == "2": 
        return 'span class="w3-tag w3-pale-blue"> II - ' + day + '</span>'
    
    else: 
        return '</i><span class="w3-tag w3-pale-blue"> III - ' + day + '</span>'
    
def html_Imc(num, edad):
    ans = ""

    if num: 
        ans = str(num)[: 5] + " (" + edad + ")"

    return ans 

def html_ImcDescripcion(num):
    ans = ""
    if num: 
        num = float(num)       
        if num < 18.5: 
            ans = '<span class="w3-tag w3-pale-blue"> Inferior </span>'
        
        elif num < 25: 
            ans = "normal"

        elif num < 30: 
            ans = "Superior"

        else: 
            ans = '<span class="w3-tag w3-pale-blue"> Obesidad </span>'

    return ans

def html_morisky(num):
    if num == "1":
        return '<i style="color:green" class="fa fa-thumbs-up"></i>'
    elif num == "0": 
        return '<i style="color:red" class="fa fa-thumbs-down"></i></span>'
    
    else: 
        return ''
    
def html_mosare(mosare):
    ans = ''
    
    if mosare: 
        ans += ' <i style="color:gray" class="fa fa-microscope"></i> '
        fecha = meses[mosare.data.month - 1] + " " + str(mosare.data.year)
        if mosare.tasa  != "":
            ans += fecha  + "<br>" + mosare.tasaDescripcion

    return ans 

def html_pie(pie):
    ans = ''
    if pie: 
        if pie.conLesion: 
            ans += ' <i style="color:red" '
        else: 
            ans += ' <i style="color:gray" '

        ans += 'class="fa fa-shoe-prints"></i> '  + meses[pie.data.month] + " " + str(pie.data.year)
  
    return ans 

def html_cardiograma(ekg):
    ans = ''
    if ekg: 
        if ekg.esNormal: 
            ans += ' <i style="color:gray" '
        else: 
            ans += ' <i style="color:red" '

        ans += 'class="fa fa-heart-pulse"></i>  '  + meses[ekg.data.month] + " " + str(ekg.data.year) 
  
    return ans 



def html_edad(fechaNacimiento, estaMuerto, fechaDeceso, format):
    ans = ''
    
    if format == 0:                 
        if estaMuerto: 
            years = ageInYears(fechaDeceso, fechaNacimiento)
            
        else: 
            years = ageInYears(date.today(), fechaNacimiento)
        
        ans += '<span class="w3-tag w3-sand">' + str(years) + ' años </span>'

    elif format == 1: 
        ans += meses[fechaNacimiento.month] + " " 
        ans += str(fechaNacimiento.year)  
        
        if format == 0: 
            ans += ""

        if estaMuerto: 
            years = ageInYears(fechaDeceso, fechaNacimiento)
            
        else: 
            years = ageInYears(date.today(), fechaNacimiento)
        
        ans += '<span class="w3-tag w3-sand">' + str(years) + ' años </span>'

    return ans 

def html_muerto(estaMuerto, fechaMuerto):
    ans = ''

    if estaMuerto:                         
        ans += '  <i style="color:black" class="fa fa-cross"></i> ' 
        ans += str(fechaMuerto.day) + ' ' 
        ans += meses[fechaMuerto.month] + " "
        ans += str(fechaMuerto.year) + '</span>'
           
    return ans 

def html_hipertension(hta, fecha):
    ans = ''

    if hta: 
        ans += '<span class="w3-tag w3-pale-yellow">Hta</span> '
        ans += '<span class="w3-tag w3-pale-yellow">' 
        if fecha.day < 10: 
            ans += "0" 
        
        ans += str(fecha.day) + " "        
        ans += meses[fecha.month] + " "
        ans += str(fecha.year) + "</span>"

    return ans 

def html_deabetes(dm, fecha):
    ans = ''

    if dm: 
        ans += '<span class="w3-tag w3-pale-red">Dm</span> '
        ans += '<span class="w3-tag w3-pale-red">' 
        if fecha.day < 10: 
            ans += "0" 
        
        ans += str(fecha.day) + " "        
        ans += meses[fecha.month] + " "
        ans += str(fecha.year) + "</span>"

    return ans 

def html_dead(muerto, fecha):
    ans = ''
    
    if muerto: 
        ans += '<span class="w3-tag w3-black"> <i style="color:white" class="fa fa-cross"></i> '
        ans += str(fecha.day) + " "        
        ans += meses[fecha.month] + " "
        ans += str(fecha.year) + "</span>"

    return ans 

def html_chequeo_icon(pie):
    ans = {}

    if pie.conLesion:         
        ans["icon"] = '<i style="color:red" class="fa fa-shoe-prints"></i>'

    else:
        ans["icon" ]= '<i style="color:grat" class="fa fa-shoe-prints"></i>'
    
    ans["day"] = pie.data.day

    ans["observacion"] = "[Chequeo de pies : " 
    ans["observacion"] += str(pie.data.day) + " "
    ans["observacion"] += meses[pie.data.month] + " "
    ans["observacion"] += str(pie.data.year) + " ]"
    if pie.conLesion:
        ans["observacion"] += "( Pies con lesión )" 
    else:
        ans["observacion"] += "( Pies sin lesión )"
    ans["observacion"] += " " + pie.observacion
 
    return ans 

def html_cardiograma_icon(ekg):
    ans = {}

    if ekg.esNormal:         
        ans["icon"] = '<i style="color:gray" class="fa fa-heart-pulse"></i>'

    else:
        ans["icon" ]= '<i style="color:red" class="fa fa-heart-pulse"></i>'
    
    ans["day"] = ekg.data.day

    ans["observacion"] = "[Electrocardiograma : " 
    ans["observacion"] += str(ekg.data.day) + " "
    ans["observacion"] += meses[ekg.data.month] + " "
    ans["observacion"] += str(ekg.data.year) + " ]"
    if ekg.esNormal:
        ans["observacion"] += "( Normal )" 
    else:
        ans["observacion"] += "( Alterado )"
    ans["observacion"] += " " + ekg.observacion
 
    return ans 

def html_selected_dotacion(num):
    ans = ''
    if num == "0":
        ans += '(Otros) dotación particular'
    
    elif num =="1":
        ans += 'I dotación'

    elif num =="2":
        ans += 'I dotación'

    elif num =="3":
        ans += 'I dotación'

    else: 
        ans += 'Número de dotación'

    return ans

def html_selected_morisky(num):
    ans = ''
    if num == "1":
        ans += 'Adecuado'
    
    elif num =="0":
        ans += 'No adecuado'

    else: 
        ans += 'Test Morisky'

    return ans

def ageInYears(date2, date1):    
    ans = date2.year - date1.year

    tmp = date(date2.year, date1.month, date1.day)

    if date2 < tmp: 
        ans -= 1 

    return ans



    




    

              
        

    







