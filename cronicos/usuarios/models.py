from django.db import models

# Create your models here.


class Enfermedad(models.Model):
    aCIE = models.CharField(default='xx.xx', primary_key = True, max_length = 5) 
    aEnfermedad = models.CharField(max_length = 100)    
    aShort = models.CharField(max_length = 10)      

    def __str__(self):
        return f"{self.aCIE} : {self.aEnfermedad}"

class Hospital(models.Model):
    id = models.CharField(default='0', primary_key = True, max_length = 1) 
    hospital = models.CharField(max_length = 20, default = "Hosp. I Urubamba")
    lugar = models.CharField(max_length = 30, default = "Urubamba")

class Paciente(models.Model):
    dni = models.CharField(primary_key = True, max_length = 10)
    nombre = models.CharField(max_length = 100)
    sexo = models.BooleanField(default = True)

    nacimiento = models.DateField(default="1950-01-01")
    historia = models.CharField(max_length = 10, default = "")
    hospital = models.ForeignKey(Hospital, on_delete = models.CASCADE, default = "0")   
    direccion = models.CharField(max_length = 50, default = "")
    celular = models.CharField(max_length = 20, default = "")

    muerto = models.BooleanField(default = False)
    fechaMuerto = models.DateField(default="2030-01-01")
    observacionMuerto = models.CharField(max_length = 100, default = "Muerto sin ninguna observación.")
    
    dm = models.BooleanField(default = False)
    fechaDm = models.DateField(default="1980-01-01")
    hta = models.BooleanField(default = False)
    fechaHta = models.DateField(default="1980-01-01")

    status = models.CharField(max_length = 1, default = True)

    observacion = models.CharField(max_length = 100, default = "")

    def __str__(self):
        return f"(DNI: {self.dni} {self.nombre})"
    
class Atencion(models.Model):
    id = models.CharField(max_length = 20, primary_key = True, default = "xxxxxxxx-xx-xxxx")
    dni = models.ForeignKey(Paciente, on_delete = models.CASCADE, default = "1")        
    dotacion = models.CharField(max_length = 1)
    fecha = models.DateField(default="1900-01-01")
    
    acto = models.CharField(max_length = 10)
    presion = models.CharField(max_length = 10)
    hemotest = models.CharField(max_length = 10, default ="")

    peso = models.CharField(max_length = 10, default="")
    talla = models.CharField(max_length = 10, default="")

    perimetro = models.CharField(max_length = 5, default ="")

    morisky = models.CharField(max_length = 1, default="0")

    imc = models.CharField(max_length = 20)
    imcDescripcion = models.CharField(max_length = 30, default="")

    edad = models.CharField(max_length = 5, default="0")

    observacion = models.CharField(max_length = 100,default="")

class Mosare(models.Model):
    id = models.CharField(max_length = 14, primary_key = True, default ="xxxxxxxx-xxxx")
    dni = models.ForeignKey(Paciente, on_delete = models.CASCADE, default = "1")     

    data = models.DateField(default="1900-01-01")

    #creatinina = models.CharField(max_length = 6, default ="")
    #tfge = models.CharField(max_length = 6, default ="")
    #albuminuria = models.CharField(max_length = 6, default ="")
    #creatinuria = models.CharField(max_length = 6, default ="")
    #tasa = models.CharField(max_length = 20, default ="")

    tamizado = models.BooleanField(default = False)

    #tamizadodescripcion = models.CharField(max_length = 20, default ="")
    descripcion = models.CharField(max_length = 20, default ="")

class Pie(models.Model):
    id = models.CharField(max_length = 20, primary_key = True, default = "xxxxxxxx-xx-xxxx")

    dni = models.ForeignKey(Paciente, on_delete = models.CASCADE, default = "00000000")    
    
    data = models.DateField(default="1900-01-01")    

    conLesion = models.BooleanField(default = False)
    observacion = models.CharField(max_length = 100, default="")

class Ekg(models.Model):
    id = models.CharField(max_length = 20, primary_key = True, default = "xxxxxxxx-xx-xxxx")
    
    dni = models.ForeignKey(Paciente, on_delete = models.CASCADE, default = "00000000")    
    
    data = models.DateField(default="1900-01-01")    

    esNormal = models.BooleanField(default = True)
    observacion = models.CharField(max_length = 100, default="")

class Especialidad(models.Model):
    id = models.CharField(max_length = 5, primary_key = True, default = "xxxxx")
    especialidad = models.CharField(max_length = 30, default = "xxxxx") 

class Referencia(models.Model):
    dni = models.ForeignKey(Paciente, on_delete = models.CASCADE, default = "1")    
    data = models.DateField(default="1900-01-01")
    especialidad = models.ForeignKey(Especialidad, on_delete = models.CASCADE, default = "1")   
    atendido =  models.BooleanField(default = False)
    observacion = models.CharField(max_length = 100, default="")

    

