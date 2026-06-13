from django.urls import path
from cursos.views import inicio, detalle_curso, crear_curso, guardar_categoria

urlpatterns = [
    path('', inicio, name='inicio'),
    path('curso/<int:curso_id>/', detalle_curso, name='detalle_curso'),
    path('curso/crear/', crear_curso, name='crear_curso'),
    path('categoria/guardar/', guardar_categoria, name='guardar_categoria'),
]