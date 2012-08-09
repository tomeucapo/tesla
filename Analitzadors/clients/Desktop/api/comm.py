#!/usr/bin/python

import socket

class commLector:
      def __init__(self, addr):
          self.addr = addr 
          try:
             self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             self.s.connect(self.addr)
	     self.s.settimeout(2)
          except Exception, e:
  	     raise Exception, "No hem puc connectar al servidor de lectures: %s" % str(e)

      def connectar(self):
          retval = True
          if(self.s.sendto("#$",self.addr)):
             data = self.s.recv(2)
             if data!="$#":
                print "No s'ha iniciat la comunicacio!"
                retval = False

          return retval 

      def enviar(self, cmd):
          retval = True
          datasnd = "$"+cmd+";\r"
          if not (self.s.sendto(datasnd,self.addr)):
             retval = False 

          return retval

      def rebre(self):
          datarcv=''
          buff=''
          while datarcv != '\r':
		try:
                   datarcv = self.s.recv(1)
		except socket.timeout:
		   break

                buff+=datarcv

          return buff.rstrip()


