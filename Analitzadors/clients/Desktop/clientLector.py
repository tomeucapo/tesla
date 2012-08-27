#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.comm import *
import sys
import pickle

if __name__ == '__main__':
   print "Lector Shell 1.9 - Tomeu Capó 2012 (C)"
   print 
   try:
      myClient = commLector((sys.argv[1],50007))
   except Exception, e:
      print str(e)
      sys.exit(-1)

   if not myClient.connectar():
      print "No puc dialogar amb el servidor!" 
      sys.exit(-1)


   print "Ready."
   acabar = False
   while not acabar:
         resp = ''
         try:
             datasnd = raw_input('] ')
         except EOFError, e:
             break

         if not datasnd:
            break;
 
         if myClient.enviar(datasnd):
               res = resp = myClient.rebre()
               cmd = datasnd.upper()

               if cmd.startswith("GET") and not cmd.startswith("GETID"):
                  if cmd.startswith("GETCONF"):
                     dom = pickle.loads(resp)
		     if cmd.endswith("XML"):
			print dom
     		        res = dom.toxml()
	             else: 
			res = dom
                  else:
	             try:
    		         res = pickle.loads(resp)
	             except ValueError, e:
			 res = resp

               print res

         if ((resp=="BYE!") or (resp=="DISCONNECTED!")):
            break

