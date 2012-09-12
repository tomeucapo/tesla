from datetime import datetime, timedelta
from django.db import models

import math

class Node(models.Model):
      nom = models.CharField(max_length=50)
      ubicacio = models.CharField(max_length=100)
      darreraLectura = models.DateTimeField()
      host = models.CharField(max_length=20)

      def __unicode__(self):
          return self.nom+" ("+self.ubicacio+")"

class Analitzador(models.Model):
      fabricant = models.CharField(max_length=40)
      model = models.CharField(max_length=40)

      def __unicode__(self):
          return self.fabricant+" "+self.model

class Parametre(models.Model):
      nom = models.CharField(max_length=4)
      descripcio = models.CharField(max_length=40)
      escala = models.FloatField()
      analitzador = models.ForeignKey(Analitzador)
      num_regs = models.IntegerField()
      unitats = models.CharField(max_length=20)
      compost = models.BooleanField()
     
      def __unicode__(self):
          return self.nom+": "+self.descripcio
 
class NodeAnalitzador(models.Model):
      node = models.ForeignKey(Node)
      analitzador = models.ForeignKey(Analitzador)
      addr = models.IntegerField()
      tlectura = models.FloatField()
      tgravacio = models.FloatField()
 
      def __unicode__(self):
          return "%s %s" % (self.node, self.analitzador)

class Lectura(models.Model):
      node = models.ForeignKey(NodeAnalitzador)
      dataHora = models.DateTimeField()

      def __unicode__(self):
            print self.dataHora
            return "%s: %s" % ( self.dataHora, self.node)     

      class Meta:
            unique_together = ('node','dataHora',)
 
class LecturaParametre(models.Model):
      lectura = models.ForeignKey(Lectura)
      parametre = models.ForeignKey(Parametre)
      valor = models.FloatField()
      vectorValors = models.CharField(max_length=512)

      def __unicode__(self):
          return self.parametre.nom

class Tarifa(models.Model):
      nom = models.CharField(max_length=40)
      node = models.ForeignKey(Node)
      dataInici = models.DateField()
      dataFi = models.DateField()
      parametre = models.ForeignKey(Parametre)
            
class FranjaHoraria(models.Model):
      tarifa = models.ForeignKey(Tarifa)
      nom = models.CharField(max_length=20)
      horaInici = models.TimeField()
      horaFi = models.TimeField()
      preu = models.FloatField()

      @property
      def hores(self):
          tdelta = datetime.strptime(self.horaFi.strftime("%H:%M:%S"), "%H:%M:%S")-datetime.strptime(self.horaInici.strftime("%H:%M:%S"), "%H:%M:%S")
          return math.ceil(tdelta.total_seconds()/60/60)
      
