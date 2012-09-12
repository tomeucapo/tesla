import time, json
from types import *

from django.core import serializers
from django.shortcuts import render_to_response
import django.contrib.auth.models as auth
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from lectures.models import Node, NodeAnalitzador, Analitzador, Lectura, LecturaParametre, Parametre 

def inici(request):
    data = {"method": request.method,
            "dataInici"  : time.strftime("01-%m-%Y", time.localtime()),
            "dataFi"  : time.strftime("%d-%m-%Y", time.localtime()),
            "var"   : "ALL",
            "lectures": True,
            "historial": True }
    
    return render_to_response("main.html", data,context_instance=RequestContext(request))


def realTime(request):
    data = {"method": request.method,
            "lectures": False,
            "historial": False }

    return render_to_response("rt.html", data,context_instance=RequestContext(request))

      
def listNodes(request, sQuery):
    nodes = []
    #print request
    for node in Node.objects.filter(nom__contains=sQuery):
        nodes.append( {"id": node.id, "nom": node.nom, "host": node.host, "ubicacio": node.ubicacio})
    
    result = { "ResultSet": {"Nodes": nodes, }}
    return HttpResponse(json.dumps(result), mimetype='application/json')

def listAnalizers(request, nodeId):
    response = HttpResponse()
    try:
        node = Node.objects.get(id=nodeId)
    except Exception, e:
        response.status_code = 400
        return response       
    except ObjectDoesNotExist, e:
        response.write("Aquest node no existeix!")
        response.status_code = 404
        return response

    nodeAnalitzadors = NodeAnalitzador.objects.filter(node=nodeId)
    analitzadors = []
    for analizer in nodeAnalitzadors:
        analitzador = Analitzador.objects.get(id=analizer.analitzador_id)
        analitzadors.append( {"id":        analizer.id,
                              "fabricant": analitzador.fabricant,
                              "model":     analitzador.model,
                              "addr":      analizer.addr})        
       
    result = {"ResultSet": {"Analitzadors": analitzadors, }}
    return HttpResponse(json.dumps(result), mimetype='application/json')
