from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from re import template


# Create your views here.


def members(request):
    #return HttpResponse("Hello world!")

    template = loader.get_template("members.html")
    
    context = {"hola": "hola mundo parte 2!!!",
    }

    return HttpResponse(template.render(context, request))
