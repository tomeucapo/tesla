#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
##########################################################################
#
# modBusComm.py
# Classe que s'encarrega de les comunicacions amb analitzadors d'energia
# que empren protocol MODBUS a travers del port serie en mode RTU.
#
# Inicialment desenvolupat per treballar amb analitzadors de la serie PMxxx
# de Groupe Schneider.
#
# Tomeu Capó
#

import serial
from crcTable import *

E_OK = 0
E_NOT_RESPONSE = 1 
E_CRC_ERROR = 2
E_SND_ERROR = 3 
E_CMD_ERROR = 4
E_NOT_OPEN_COMM = 5

READ_WORDS  = 3
READ_E_WORDS = 4
WRITE_WORDS = 16
WRITE_WORD  = 6
DIAG_EXCHNG = 8
REPOR_SLAVE = 17
IDENT_DSP   = 43

msgErrors = {E_NOT_RESPONSE: "El dispositiu no reson, ho tonare a provar",
             E_CRC_ERROR:    "La trama rebuda es erronea, error de CRC!",
             E_SND_ERROR:    "No puc enviar la trama al dispositiu",
             E_CMD_ERROR:    "Error de la comanda",
             E_NOT_OPEN_COMM: "El port de comunicacions no esta obert",}

msgCmdError = ["Funcio invalida",
               "Adreca invalida",
               "Valor incorrecte",
               "Error al dispositiu esclau",
               "L'esclau ha acceptat la peticio",
               "Esclau ocupat",
               "L'esclau no ha acceptat la peticio",
               "Error de paritat de memoria"]

class codeFuncNotValid(Exception):
      pass

class modBusComm:
    def __init__(self, addrSlave, dsp):
        self.id = addrSlave
        self.adrecaEsclau = addrSlave
        (self.serie, self.mutex) = dsp
        self.lastCmd = ''
        self.lastResponse = ''
        self.lastSize = 0
        self.lastError = E_OK
        self.lastErrorCmd = -1 
        self.logger = None

    # Metode que envia una trama en format ModBUS RTU

    def enviar(self, op, addr, size, data=None):
        retval = True

        if op not in [READ_E_WORDS, READ_WORDS, WRITE_WORDS, REPOR_SLAVE]:
           raise codeFuncNotValid("Code function not valid")

        if not self.serie.isOpen():
           self.lastError = E_NOT_OPEN_COMM
           return False
        
        self.lastSize = size
       
        # @ del esclau i l'operacio 

        sndtxt = chr(self.adrecaEsclau)+chr(op) 

        # Depenent del tipus d'operacio que tinguem la trama te una forma o un altre

        if op in [READ_E_WORDS, READ_WORDS, WRITE_WORDS]:        
           sndtxt += chr((addr - 1) >> 8)
           sndtxt += chr((addr - 1) & 0xff)
           sndtxt += chr(size >> 8)
           sndtxt += chr(size & 0xff) 

        if op == WRITE_WORDS and data:
           sndtxt += chr(len(data)%256)
           for byte in data:
               sndtxt += chr(byte)
            
        # Calculam el CRC de la trama construida
        
        crc = CRC16(sndtxt)
        sndtxt += chr(crc >> 8)
        sndtxt += chr(crc & 0xFF)
        
        self.lastCmd = op 
        self.lastError = E_OK
        self.logger.debug("[ TX ] "+' '.join(["%(vc)02X" % {"vc": ord(c)} for c in sndtxt]))         

        try:
            self.serie.write(sndtxt)
        except serial.serialutil.SerialException, e:
            self.logger.error("enviar: %s" % str(e))
            self.lastError = E_SND_ERROR
            retval = False      
                      
        return(retval)           

    def resetConnection(self):
        if self.serie.isOpen():
           self.serie.close()
           
        try:
           self.serie.open()
        except serial.serialutil.SerialException, e:
           self.logger.error("Obrint el port serie: %s" % str(e))
           
    def __flushBuffers__(self):
        self.serie.flushInput()
        self.serie.flushOutput()

    # Metode que ens permet rebre una trama ModBUS RTU i extreure informacio
    
    def rebre(self):
        retval = True

        if not self.serie.isOpen():
           self.lastError = E_NOT_OPEN_COMM
           return False
        
        try:
            respHead = self.serie.read(3)
        except serial.serialutil.SerialException, e:
            self.logger.error(str(e))
            self.lastError = E_CMD_ERROR 
            return False

        frameRx = respHead

        # Si a la capsalera hi ha res. Recordam que el metode read
        # te un timeout. Normalment basta si l'esclau esta funcionant correctament.

        if len(respHead) < 2:
           self.__flushBuffers__()
           self.lastError = E_NOT_RESPONSE
           return False
 
        # Determinam si es la resposta de la peticio feta anteriorment
        # hem de pensar que primer enviam una consulta i ens possam amb mode
        # d'escolta.

        retCode = ord(respHead[1])

        if (retCode != self.lastCmd):
            self.__flushBuffers__()
            self.lastError = E_CMD_ERROR
            self.lastErrorCmd = 0 #ord(resp[2])-1
            return False
 
        lenData = ord(respHead[2]) 
        self.lastResponse = []
        self.lastResponseB = ''
        
        # Extreim la informacio de la trama. Tenim dos atributs:
        # lastResponseB: Conte la informacio en format cru.
        # lastResponse: Conte una llista dels valors.
        
        i = 0
        while i < lenData:
                try:
                    resp = self.serie.read(2)
                except serial.serialutil.SerialException, e: 
                    self.logger.error(str(e))
                    break
  
                if len(resp) < 2:
                    break

                frameRx += resp 
                value = (ord(resp[0]) << 8) | ord(resp[1])
                self.lastResponseB += resp
                self.lastResponse.append(value)
                i += 2

        if i == 0:
           self.__flushBuffers__()
           self.lastError = E_NOT_RESPONSE 
           return False
        
        # Llegim els dos bytes de la coa (CRC)

        try:
            respTail = self.serie.read(2)
        except serial.serialutil.SerialException, e:
            self.logger.error(str(e))
            self.__flushBuffers__()
            self.lastError = E_NOT_RESPONSE
            return False

        frameRx += respTail
        
        self.logger.debug("[ RX ] " + ' '.join(["%(vc)02X" % {"vc": ord(c)} for c in frameRx]))

        # Calculam el CRC en base a la informacio rebuda fins ara
        # i verificam que sigui el mateix que rebem del esclau.

        if len(respTail) < 2:
           self.lastError = E_CRC_ERROR
           return False
        
        crcRx = (ord(respTail[0]) << 8) | ord(respTail[1])
        crcCa = CRC16(frameRx[:-2])

        if crcRx != crcCa:
            self.lastError = E_CRC_ERROR
            retval = False
        else:
            self.lastError = E_OK
            self.lastErrorCmd = -1 
       
        return retval

    @property
    def lastBigIntValue(self):
        return reduce(lambda x, y:x << 8 | y, [ord(c) for c in self.lastResponseB])

    @property
    def lastStrValue(self):
        return self.lastResponseB

    def msgError(self):
        msgCmdErr = ""
        if self.lastError > 0:
            if self.lastErrorCmd >= 0:
                msgCmdErr = "(" + msgCmdError[self.lastErrorCmd] + ")"
                return(msgErrors[self.lastError] + " " + msgCmdErr)     
            else:
                return(msgErrors[self.lastError])

  
