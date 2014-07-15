import time, json
from types import *

from django.core import serializers
from django.shortcuts import render_to_response
import django.contrib.auth.models as auth
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, date, time

from teslaweb.lectures.models import Node, NodeAnalitzador, Analitzador, Lectura, LecturaParametre, Parametre 


def consulta(request):
       
    data = {"method": request.method,
            "num_reserves": numReserves}

    return render_to_response("main.html", data,context_instance=RequestContext(request))
    
    
