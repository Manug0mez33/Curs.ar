from django.contrib import admin
from .models import Categoria, Curso, Modulo, Clase, Inscripcion, Resena

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'instructor', 'categoria', 'precio', 'duracion')
    list_filter = ('categoria', 'instructor')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('instructor',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.instructor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'orden')
    list_filter = ('curso',)
    search_fields = ('titulo',)

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'orden')
    list_filter = ('modulo',)
    search_fields = ('titulo',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'fecha_inscripcion')
    list_filter = ('curso', 'fecha_inscripcion')
    search_fields = ('usuario__username', 'curso__titulo')
    readonly_fields = ('fecha_inscripcion',)

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'calificacion', 'fecha')
    list_filter = ('calificacion', 'curso', 'fecha')
    search_fields = ('usuario__username', 'curso__titulo', 'comentario')
    readonly_fields = ('fecha',)



