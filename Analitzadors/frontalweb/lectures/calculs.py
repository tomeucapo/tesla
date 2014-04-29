
import json
from types import *

from django.core import serializers
from django.shortcuts import render_to_response
import django.contrib.auth.models as auth
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist


from lectures.models import Node, NodeAnalitzador, Analitzador, Lectura, LecturaParametre, Parametre, FranjaHoraria

#from datetime import datetime , date, time
import time
from datetime import datetime

def inici(request):
    data = {"method": request.method,
            "dataInici"  : time.strftime("01-%m-%Y", time.localtime()),
            "dataFi"  : time.strftime("%d-%m-%Y", time.localtime()),
            "lectures"   : False,
            "historial"  : True }
    
    return render_to_response("costs.html", data,context_instance=RequestContext(request))

def costsTarifes(request, dataInici, dataFi, nodeAnalitzadorId):
    retval = HttpResponse()
    
    try:
          dataIniciP = datetime.strptime(dataInici, "%d-%m-%Y")         
          dataFiP = datetime.strptime(dataFi, "%d-%m-%Y")         
    except Exception, e:
          retval.status_code = 400
          retval.write(str(e))
          return retval
    
    try:
         nodeAnalizador = NodeAnalitzador.objects.get(id=nodeAnalitzadorId)
    except ObjectDoesNotExist, e:   
         retval.status_code = 404
         retval.write(str(e))
         return retval
    except Exception, e:
         retval.status_code = 400
         retval.write(str(e))
         return retval
        
    potFranjes = {}
    
    franjes = FranjaHoraria.objects.filter(tarifa__node__nodeanalitzador=nodeAnalitzadorId)
    parTarifa = franjes[0].tarifa.parametre

    if len(franjes) == 0:
       retval.status_code = 404
       retval.write("Ho ni ha franjes horaries definides per aquest analitzador!")
       return retval

    dataIniciL = datetime.strptime(dataInici+" 00:00:00", "%d-%m-%Y %H:%M:%S")         
    dataFiL = datetime.strptime(dataFi+" 23:59:59", "%d-%m-%Y %H:%M:%S")
    
    lectures = LecturaParametre.objects.filter(lectura__node=nodeAnalitzadorId).filter(parametre__nom=parTarifa.nom).filter(lectura__dataHora__range=(dataIniciL, dataFiL)).order_by("lectura__dataHora")
    
    if len(lectures) == 0:
       retval.status_code = 404
       retval.write("Ho ni ha lectures de la variable (%s) en les dates compreses!" % parTarifa.descripcio)
       return retval

    lTarifes = {}   
    for l in lectures:
        horaLectura = l.lectura.dataHora.time()
        dataLectura = l.lectura.dataHora.date()
        
        franjaLectura = franjes.filter(tarifa__dataInici__lte=dataLectura).filter(tarifa__dataFi__gte=dataLectura)
        franja = franjaLectura.filter(horaInici__lte=horaLectura).filter(horaFi__gte=horaLectura)        

        if not franja:
           retval.status_code = 404
           retval.write("Ho ni franjes horaries configurades per aquest analitzador en eaquestes hores")
           return retval
        
        nomTarifa = franja[0].nom
        preuTarifa = franja[0].preu
        horesTarifa = franja[0].hores

        if nomTarifa not in lTarifes.keys():
           lTarifes[nomTarifa] = horesTarifa  
        else:
           lTarifes[nomTarifa] += horesTarifa

        if dataLectura not in potFranjes.keys():
           potFranjes[dataLectura] = {}

        liniaDia = potFranjes[dataLectura]
        if nomTarifa not in liniaDia.keys():
           potFranjes[dataLectura][nomTarifa] = {"total": l.valor, "preu": preuTarifa, "lectures": 1, "horesTarifa": horesTarifa}
        else:
           liniaDia[nomTarifa]["horesTarifa"] += horesTarifa
           liniaDia[nomTarifa]["total"] += l.valor
           liniaDia[nomTarifa]["lectures"] += 1 

    resultat = {"ResultSet": {"Linies": [], }}

    for dataLectura, tarifa in potFranjes.iteritems():
        linia = {"data": dataLectura.strftime("%d-%m-%Y"), "consumTotal": 0}
        consumTotal = 0
        costTotal = 0
        for t, conf in tarifa.iteritems():
            consum = (conf["total"]/conf["lectures"])*conf["horesTarifa"]
            linia[str(t)] = {"import": "%.2f" % float(consum*conf["preu"]), "consum": "%.2f" % float(consum), "horesTarifa": conf["horesTarifa"]}
            consumTotal += consum
            costTotal += (consum*conf["preu"])
            
        linia["consumTotal"] = "%.2f" % float(consumTotal)
        linia["costTotal"] = "%.2f" % float(costTotal)
        
        resultat["ResultSet"]["Linies"].append(linia)
    
    return HttpResponse(json.dumps(resultat),mimetype='application/json')
    
    
