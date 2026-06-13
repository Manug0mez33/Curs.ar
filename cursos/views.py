from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from cursos.models import Curso, Categoria
from cursos.forms import CursoForm


def inicio(request):
    cursos = Curso.objects.select_related('categoria').all()
    return render(request, 'cursos/inicio.html', {'cursos': cursos})

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, 'cursos/detalle_curso.html', {'curso': curso})

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:    
        form = CursoForm()
    
    categorias = Categoria.objects.all()
    return render(request, 'cursos/crear_curso.html', {'form': form, 'categorias': categorias})

@login_required
def guardar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre and not Categoria.objects.filter(nombre=nombre).exists():
            Categoria.objects.create(nombre=nombre)
    return redirect('crear_curso')