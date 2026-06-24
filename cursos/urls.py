from django.urls import path
from cursos.views import (
    inicio, detalle_curso, crear_curso, guardar_categoria, inscribirse, contenido_curso, eliminar_curso,
    listar_modulos, crear_modulo, editar_modulo, eliminar_modulo,
    crear_clase, editar_clase, eliminar_clase
)

urlpatterns = [
    path('', inicio, name='inicio'),
    path('curso/<int:curso_id>/', detalle_curso, name='detalle_curso'),
    path('curso/<int:curso_id>/inscribirse/', inscribirse, name='inscribirse'),
    path('curso/<int:curso_id>/contenido/', contenido_curso, name='contenido_curso'),
    path('curso/crear/', crear_curso, name='crear_curso'),
    path('curso/<int:curso_id>/eliminar/', eliminar_curso, name='eliminar_curso'),
    path('categoria/guardar/', guardar_categoria, name='guardar_categoria'),
    
    # URLs de Módulos
    path('curso/<int:curso_id>/modulos/', listar_modulos, name='listar_modulos'),
    path('curso/<int:curso_id>/modulos/crear/', crear_modulo, name='crear_modulo'),
    path('modulo/<int:modulo_id>/editar/', editar_modulo, name='editar_modulo'),
    path('modulo/<int:modulo_id>/eliminar/', eliminar_modulo, name='eliminar_modulo'),
    
    # URLs de Clases
    path('modulo/<int:modulo_id>/clase/crear/', crear_clase, name='crear_clase'),
    path('clase/<int:clase_id>/editar/', editar_clase, name='editar_clase'),
    path('clase/<int:clase_id>/eliminar/', eliminar_clase, name='eliminar_clase'),
]