from django.contrib import admin

# Register your models here.

from .models import Paciente
from .models import Enfermedad
from .models import Atencion
from .models import Mosare
from .models import Pie
from .models import Ekg
from .models import Referencia
from .models import Especialidad
from .models import Hospital

# Register your models here.
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("id", "hospital", "lugar")

class PacienteAdmin(admin.ModelAdmin):
    list_display = ("dni", "nombre","muerto","hta","dm", "status")

class AtencionAdmin(admin.ModelAdmin):
    list_display = ("id","dni", "fecha", "dotacion")

class PieAdmin(admin.ModelAdmin):
    list_display = ("id","data","conLesion", "observacion")

class EkgAdmin(admin.ModelAdmin):
    list_display = ("id","data","esNormal", "observacion")

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("id","especialidad")
    
#class MosareAdmin(admin.ModelAdmin):
#    list_display = ("id","dni", "data", "tamizado" "descripcion")

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Atencion, AtencionAdmin)
admin.site.register(Pie, PieAdmin)
admin.site.register(Ekg, EkgAdmin )
admin.site.register(Enfermedad)
#admin.site.register(Mosare, MosareAdmin)
admin.site.register(Mosare)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Referencia)






