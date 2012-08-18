

import time, threading, socket, Queue, re
import logging, logging.config

HOST = ''
PORT = 50007
MAX_RCV_BUFF = 20

VALID_CMD = ["QUIT", "SHUTDOWN", "START", "STARTALL", "PAUSE", "RESUME", "RELOAD", 
             "STATUS", "GETID", "GETVARS", "GETDEFS", "GETSTATUS", 
             "FORCEREQ", "GETCONF", "IDENT", "SETQUERY",
             "HELP"]

class server(threading.Thread):
      def __init__(self, qRequest, qResponse):
          self.logger = logging.getLogger('lector.srvtcp')

          self.__queue = qRequest
          self.__queueResponse = qResponse

          threading.Thread.__init__(self, name=self.__class__.__name__)
          try:
             self.socketSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             self.socketSrv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          except:
             raise IOError, "No puc crear el socket del servidor ..."
             pass

          self.lastCmd = ("", "")
          self.aturaTot = False
          self.clients = []
          
      def recvCmd(self, clientSock):
          buff = ''
          data = clientSock.recv(1)
          if len(data)<1:
             raise Exception, "Trama rebuda buida"

          while data != '\r' and len(buff)<MAX_RCV_BUFF:
                buff += data
                data = clientSock.recv(1)

          if len(data)>MAX_RCV_BUFF:
             raise Exception, "Trama rebuda massa grossa"

          return buff

      def parseCmd(self, data):
          data = data.upper().rstrip()
          cmdTrobada = re.search(r"^\$([A-Z]+)(?:|.)([A-Z0-9]*)\;", data)
          
          self.lastCmd = (None, None)
          if cmdTrobada:
             self.lastCmd = cmdTrobada.groups()          
          
          return cmdTrobada 

      def beginDialog(self, conn):
          ini = conn.recv(2)
          if ini == '#$':
             conn.send('$#')
          return(ini == '#$')

      def handleClient(self, clientSock):
          peer = clientSock.getpeername()
          numFormatErr = 0
          numCmdErr = 0

          try:
              if not self.beginDialog(clientSock):
                 return
          except Exception, e:
              self.logger.error(str(e))
              clientSock.close()
              return

          connectat = True
          while connectat:              
              try:
                 data = self.recvCmd(clientSock)
              except socket.timeout:
                 self.logger.error("Client timeout")
                 break
              except socket.error:
                 self.logger.error("Client shutdown")
                 return
              except Exception, e:
                 self.logger.error(str(e))
                 break
              if not len(data):
                 break

              if numFormatErr > 10 or numCmdErr > 10:
                 self.logger.error("El client s'ha excedit amb el nombre de comandes erronees")
                 connectat = False
                 break

              if not self.parseCmd(data):
                 self.logger.error("Invalid format command (%d)" % numFormatErr)
                 clientSock.send("FORMAT_ERROR\r")
                 numFormatErr+=1
                 continue

              self.currConn = clientSock
              try:
                 (cmd, args) = self.lastCmd
              except ValueError, e:                 
                 self.logger.error("Error en agafar la darrera comanda")
                 break
            
              if not cmd in VALID_CMD:
                 self.logger.error("Invalid command (%d)" % numCmdErr)
                 clientSock.send("ERR\r")
                 numCmdErr+=1
                 continue
              
              self.logger.debug("Received command %s ..." % cmd)
              
              if cmd == 'SHUTDOWN':
                 self.aturaTot = True
                 connectat = False 
              else:
                 if cmd == 'QUIT':
                    connectat = False
                 else:
                    if cmd == 'HELP':
                       clientSock.send(" ".join(VALID_CMD))
                       clientSock.send("\r")
                       continue
              
              if self.__queue.full():
                 self.logger.error("Receive queue is full!")
                 clientSock.send("MAX_CLIENTS\r")
                 connectat = False
                 break
            
              self.__queue.put((self.lastCmd, clientSock))
              self.logger.debug("Command %s enqueued... (%d)" % (cmd, self.__queue.qsize()) )
              
          clientSock.send("DISCONNECTED!\r")
          self.logger.debug("Client desconnectat ...")
          clientSock.close()

      def sendResponses(self):
          self.logger.debug("Starting response dispacher ...")
          while not self.aturaTot:
                self.logger.debug("sendResponses: Waiting for next event ...")
          
                (cmd, sockCli, response) = self.__queueResponse.get(block=True)
                
                self.logger.debug("Send response from command %s" % cmd)
                try:
                   sockCli.send("%s\r" % response)
                except socket.error, e:
                   self.logger.error("Enviant resposta: %s" % str(e))
                   time.sleep(0.5)
                   continue
  
                self.logger.debug("Finish send response ...")
                self.__queueResponse.task_done()
                
      def __disconnectAllClients__(self):
          self.socketSrv.close()
          for sock in self.clients:
              sock.close()
 
      def run(self):
          self.logger.info("Starting TCP Server ...")
          try:
             self.socketSrv.bind((HOST, PORT))
             self.socketSrv.listen(100)
          except:
             raise IOError, "Aquest socket ja esta agafat per algu altre"
          
          tReponse = threading.Thread(target = self.sendResponses)
          tReponse.setDaemon(1)
          tReponse.start()
          
          while not self.aturaTot:
                try:
                    clientSock, clientAddr = self.socketSrv.accept()
                    clientSock.settimeout(300)
                except KeyboardInterrupt:
                    self.__disconnectAllClients__()
                    break
                except:
                    traceback.print_exc()
                    continue

                self.logger.debug("Client connectat %(add)s... " % {"add": clientAddr})

                self.clients.append(clientSock)
                t = threading.Thread(target = self.handleClient, args = [clientSock])
                t.setDaemon(1)
                t.start()
          
          tReponse.join()         
          self.__disconnectAllClients__()
          self.socketSrv.close()    
