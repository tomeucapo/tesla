from teslaweb.lectures.models import * 
from django.contrib import admin

class ParametreInline(admin.TabularInline):
      model = Parametre
 
class AnalitzadorAdmin(admin.ModelAdmin):
    list_display = ('model','fabricant')
    inlines = [ParametreInline, ]
     
class ParametreAdmin(admin.ModelAdmin):
    list_display = ('nom','descripcio','escala')

class NodeInline(admin.TabularInline):
    model = NodeAnalitzador
    extra = 3

class NodeAdmin(admin.ModelAdmin):
    list_display = ['nom','ubicacio','host']
    inlines = [NodeInline, ]

class LecturaParametreInline(admin.TabularInline):
    model = LecturaParametre 
    extra = 3

class LecturaAdmin(admin.ModelAdmin):
    inlines = [LecturaParametreInline, ]

class FranjaHorariaInline(admin.TabularInline):
      model = FranjaHoraria
      extra = 2
 
class TarifaAdmin(admin.ModelAdmin):
      list_display = ['nom','dataInici','dataFi',]
      inlines = [FranjaHorariaInline, ]

admin.site.register(Analitzador, AnalitzadorAdmin)
admin.site.register(Parametre, ParametreAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Lectura, LecturaAdmin)
admin.site.register(Tarifa, TarifaAdmin)
