from django.contrib import admin
from .models import UsuarioPersonalizado

@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nombre', 'apellido', 'es_instructor')
    list_filter = ('es_instructor',)
    search_fields = ('username', 'email', 'nombre', 'apellido')

