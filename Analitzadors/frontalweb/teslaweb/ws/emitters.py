"""
   emitters.py

   Modul on definim les classes que empram per formatar les respostes
   del nostre servei RESTful.
"""

from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_unicode
from piston.emitters import Emitter
import StringIO

"""
    Classe que ens formata la sortida de disponibilitat en XML
"""
"""
class XMLDispoEmitter(Emitter):
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("bicicleta", {})
                self._to_xml(xml, item)
                xml.endElement("bicicleta")
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                if key != '_state':
                   xml.startElement(key, {})
                   self._to_xml(xml, value)
                   xml.endElement(key)
        else:
            xml.characters(smart_unicode(data))

    def render(self, request):
        stream = StringIO.StringIO()
        
        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement("dispo", {})
        
        self._to_xml(xml, self.construct())
        
        xml.endElement("dispo")
        xml.endDocument()
        
        return stream.getvalue()

# Registram els emissors que hem d'emprar

Emitter.register('xml', XMLDispoEmitter, 'text/xml; charset=utf-8')

"""
