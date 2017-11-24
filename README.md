# Tesla Analyzer

Given the great need of energy saving due to the rising price of KW, and try to educate the consumer smart energy companies. 
We look for preventive monitoring systems electricity consumption, so that this can be a more correct action and make optimum 
use of electricity. 
So this project is focused on developing a system to acquire electric measurements, and so can make a cost estimate equivalent 
considering relevant rates to calculate their cost. In the market there are many proprietary solutions (not open) that involve 
a high cost additional licenses, which are often not tolerable for the company, so we aim to provide an open system which can 
integrate different solutions into a single hardware system for monitoring and analysis of both measures to be totally flexible 
to implement integrations with web services that use rise from websites, mobile applications in mobile and tablets. As well as 
being flexible also be integrated with other hardware solutions for the electric measurements, and thus provide a comprehensive 
and open solution. 

## Supported data adquisition device drivers 

* Circutor CVMk
* Schneider-Electric PM-710, 500
* Desin DAS-8000

## Server

### Usage

#### Base configuration
The server needs a basic configuration file called lector.ini, same as:
```ini
[General]
log_level=debug
auto_start=yes
log_dir=log
```
This configuration determines is lectorSrv autostart or not, and configure main log level and/or log dir.

#### Server configuration file
For start the server process for adquisition data you need create an configure device configuration file (config.xml), at the same directory of the server, like this:
```xml
<?xml version='1.0' encoding='UTF-8'?>                                                                      
<configuracio>                                                                                              
  <node id="4" name="CIFP Joan Taix" location="Sa Pobla (Son Basca)" />                                     
  <devices>                                                                                                 
      <device id="1" type="serial" enabled="true">                                                          
         <port>COM1:</port>                                                                                 
         <baud>19200</baud>                                                                                 
         <bits>8</bits>                                                                                     
         <timeout>1</timeout>                                                                               
         <parity>N</parity>                                                                                 
      </device>                                                                                             
      <device id="2" type="serial" enabled="true">                                                          
         <port>COM4:</port>                                                                                 
         <baud>38400</baud>                                                                                 
         <bits>8</bits>                                                                                     
         <timeout>4</timeout>                                                                               
         <parity>N</parity>                                                                                 
      </device>                                                                                             
  </devices>                                                                                                
  <equips>                                                                                                  
    <analitzador id="1" device="1" model="PM710" driver="modBusComm" dataDriver="pmData">                   
        <params>                                                                                            
                <fabricant>Schneider</fabricant>                                                            
                <model>PM710</model>                                                                        
                <tempsgravacio>15</tempsgravacio>                                                           
                <tempslectura>60</tempslectura>                                                             
        </params>                                                                                           
                                                                                                            
        <dataexports>                                                                                       
            <dataexport type="localFile" target="dades" />                                                  
            <!-- <dataexport type="clientRest" target="http://tesla.botilla.net/central/ws" /> -->          
        </dataexports>                                                                                      
                                                                                                            
        <peticions>                                                                                         
         <consulta>TPF</consulta>                                                                           
         <consulta>IPF</consulta>                                                                           
         <consulta>FRE</consulta>                                                                           
         <consulta>PAF</consulta>                                                                           
         <consulta>PAT</consulta>                                                                           
         <consulta>PRT</consulta>                                                                           
         <consulta>FPT</consulta>                                                                           
         <consulta>THDV</consulta>                                                                          
         <consulta>CEA</consulta>                                                                           
         <consulta>CER</consulta>                                                                           
        </peticions>                                                                                        
   </analitzador>     
   </equips>
```

#### Command line server

Can start may server process with lector.py main program, this type of start working in foreground mode and waiting a Ctrl+C signal for interrupt all processes, used on development environments.

#### Windows Service

For install server as windows service you need use lectorSvc.py, this uses a Win32 API for install, start, stop and uninstall process. Needs copy lector.ini initial configuration file to Windows directory.

## Client

### Command line client

Simple command line shell for sends commands to server.

### GUI Client

Based on PyQt library, and can connect to a server and reads al measurements of all power analizers in realtime. Can control aquisition server: Pause and resume remotely.

### API Client library

This a simple python library for connect to server and control this.

## Web application and webservice

This part of project contains a Django application that manage central database for collect all data from different Lector Servers and have an REST webservice implemented with Django-Tastypie.

### API REST

This API allows the servers to send the readings to the central server for later analysis. This API have two differnet calls:

* GET /ws/v2/history/load
* POST /ws/v2/history/save

The lector server uses POST save method for send all measurements to this service.
