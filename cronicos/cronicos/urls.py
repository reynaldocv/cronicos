"""
URL configuration for cronicos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from usuarios.views.pacientes import *
from usuarios.views.atenciones import *
from usuarios.views.reporters import *
from usuarios.views import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', resumen, name = 'resumen'),
    
    path('<str:_dni>/<str:_year>', pacienteDniYear, name = "pacienteDniYear"),
    path('<str:_dni>/<str:_year>/<str:_option>', pacienteOption, name = "pacienteOption"),    
    path('<str:_dni>/'    , pacienteDni     , name = "pacienteDni"),    

    path('pacientes/list/', pacientes_list  , name = 'pacientes_list'),

    path('paciente/new/'  , paciente_new    , name = 'paciente_new'),
    path('paciente/add/'  , paciente_add    , name = 'paciente_add'),
    path('paciente/mod/'  , paciente_mod    , name = 'paciente_mod'),
    path('paciente/alter/', paciente_alter  , name = 'paciente_alter'),    
    path('paciente/kill/' , paciente_kill   , name = 'paciente_kill'),  

    path('muertos/list/'  , muertos_list    , name = 'muertos_list'),
    
    path('muerto/mod/'    , muerto_mod      , name = 'muerto_mod'),
    path('muerto/alter/'  , muerto_alter    , name = 'muerto_alter'),

    path('dotacion/new/'  , dotacion_new    , name = 'dotacion_new'),
    path('dotacion/add/'  , dotacion_add    , name = 'dotacion_add'),
    path('dotacion/mod/'  , dotacion_mod    , name = 'dotacion_mod'),
    path('dotacion/alter/', dotacion_alter  , name = 'dotacion_alter'),

    path('ekg/new/'       , ekg_new         , name = 'ekg_new'),
    path('ekg/add/'       , ekg_add         , name = 'ekg_add'),
    path('ekg/mod/'       , ekg_mod         , name = 'ekg_mod'),
    path('ekg/alter/'     , ekg_alter       , name = 'ekg_alter'),

    path('pie/new/'       , pie_new         , name = 'pie_new'),
    path('pie/add/'       , pie_add         , name = 'pie_add'),
    path('pie/mod/'       , pie_mod         , name = 'pie_mod'),
    path('pie/alter/'     , pie_alter       , name = 'pie_alter'),

    path("mosare/add/"    , mosare_add      , name = "mosare_add"),
   
    path("referencia/add/"  , referencia_add  , name = "referencia_add"),
    path("referencia/mod/"  , referencia_mod  , name = "referencia_mod"),
    path("referencia/alter/", referencia_alter, name = "referencia_alter"),

    path("superAdmin", super_admin, name = "super_admin"),

] 