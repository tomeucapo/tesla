
import threading, json, time
from api.client import *

def client(numCli):
    rError = 0
    try:
    	lector = ctrlLector(("localhost", 50007))
        fitxer = open("thread_%d.txt" % threading.current_thread().ident,"w")
	tempsTotal = 0.0
        for r in range(100):
            rError = r
	    fitxer.write("Request %d:%d ****************************************************************************************\n" % (numCli, r))
            tIni = time.time()
            fitxer.write("ID = %s\n" % lector.getId(1))
            fitxer.write("VARS = %s\n" % json.dumps(lector.getVars(1))) 
            tempsTotal += (time.time()-tIni)
	tempsMitg = tempsTotal/100

    	lector.desconnecta()
        fitxer.close()
	print "Client %d, acabat! (%3.7f)" % (numCli, tempsMitg)
    except Exception, e:
        print "(%d, %d): %s" % (numCli, rError, str(e))

threads = []
for i in range(100):
    t = threading.Thread(target = client, args = [i])
    t.setDaemon(1)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
