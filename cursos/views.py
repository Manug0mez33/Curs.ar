from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cursos.models import Curso, Categoria, Inscripcion, Modulo, Clase, Resena
from cursos.forms import CursoForm, ModuloForm, ClaseForm, ResenaForm


def inicio(request):
    cursos = Curso.objects.select_related('categoria').all()
    return render(request, 'cursos/inicio.html', {'cursos': cursos})

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    inscripto = False
    resena_existente = None
    
    if request.user.is_authenticated:
        inscripto = Inscripcion.objects.filter(usuario=request.user, curso=curso).exists()
        if inscripto:
            resena_existente = Resena.objects.filter(usuario=request.user, curso=curso).first()
    
    return render(request, 'cursos/detalle_curso.html', {
        'curso': curso,
        'inscripto': inscripto,
        'resena_existente': resena_existente
    })

@login_required
def inscribirse(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    inscripcion, created = Inscripcion.objects.get_or_create(
        usuario=request.user,
        curso=curso
    )
    
    if created:
        messages.success(request, f'¡Te has inscripto en {curso.titulo}!')
    else:
        messages.info(request, f'Ya estabas inscripto en {curso.titulo}')

    return redirect('contenido_curso', curso_id=curso_id)

@login_required
def contenido_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    inscripcion = Inscripcion.objects.filter(usuario=request.user, curso=curso).first()
    if not inscripcion:
        messages.error(request, 'Debes estar inscripto en el curso para ver su contenido')
        return redirect('detalle_curso', curso_id=curso_id)
    
    modulos = curso.modulos.all()
    return render(request, 'cursos/contenido_curso.html', {
        'curso': curso,
        'modulos': modulos
    })

@login_required

def crear_curso(request):
    if not request.user.es_instructor:
        messages.error(request, 'Solo los instructores pueden crear cursos')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.instructor = request.user
            curso.save()
            messages.success(request, 'Curso creado exitosamente')
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

@login_required
def eliminar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    if curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para eliminar este curso')
        return redirect('inicio')
    
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado exitosamente')
        return redirect('inicio')
    
    return render(request, 'cursos/confirmar_eliminar_curso.html', {
        'curso': curso
    })




@login_required
def listar_modulos(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    if curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para ver este curso')
        return redirect('inicio')
    
    modulos = curso.modulos.all()
    return render(request, 'cursos/listar_modulos.html', {
        'curso': curso,
        'modulos': modulos
    })

@login_required
def crear_modulo(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    if curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para crear módulos en este curso')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        if form.is_valid():
            modulo = form.save(commit=False)
            modulo.curso = curso
            modulo.save()
            messages.success(request, 'Módulo creado exitosamente')
            return redirect('listar_modulos', curso_id=curso_id)
    else:
        form = ModuloForm()
    
    return render(request, 'cursos/crear_modulo.html', {
        'form': form,
        'curso': curso
    })

@login_required
def editar_modulo(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    
    if modulo.curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para editar este módulo')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = ModuloForm(request.POST, instance=modulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Módulo actualizado exitosamente')
            return redirect('listar_modulos', curso_id=modulo.curso.id)
    else:
        form = ModuloForm(instance=modulo)
    
    return render(request, 'cursos/editar_modulo.html', {
        'form': form,
        'modulo': modulo,
        'curso': modulo.curso
    })

@login_required
def eliminar_modulo(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    
    if modulo.curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para eliminar este módulo')
        return redirect('inicio')
    
    curso_id = modulo.curso.id
    
    if request.method == 'POST':
        modulo.delete()
        messages.success(request, 'Módulo eliminado exitosamente')
        return redirect('listar_modulos', curso_id=curso_id)
    
    return render(request, 'cursos/confirmar_eliminar_modulo.html', {
        'modulo': modulo,
        'curso': modulo.curso
    })




@login_required
def crear_clase(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    
    if modulo.curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para crear clases en este módulo')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = ClaseForm(request.POST)
        if form.is_valid():
            clase = form.save(commit=False)
            clase.modulo = modulo
            clase.save()
            messages.success(request, 'Clase creada exitosamente')
            return redirect('listar_modulos', curso_id=modulo.curso.id)
    else:
        form = ClaseForm()
    
    return render(request, 'cursos/crear_clase.html', {
        'form': form,
        'modulo': modulo,
        'curso': modulo.curso
    })

@login_required
def editar_clase(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    
    if clase.modulo.curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para editar esta clase')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clase actualizada exitosamente')
            return redirect('listar_modulos', curso_id=clase.modulo.curso.id)
    else:
        form = ClaseForm(instance=clase)
    
    return render(request, 'cursos/editar_clase.html', {
        'form': form,
        'clase': clase,
        'modulo': clase.modulo,
        'curso': clase.modulo.curso
    })

@login_required
def eliminar_clase(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    
    if clase.modulo.curso.instructor != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta clase')
        return redirect('inicio')
    
    curso_id = clase.modulo.curso.id
    
    if request.method == 'POST':
        clase.delete()
        messages.success(request, 'Clase eliminada exitosamente')
        return redirect('listar_modulos', curso_id=curso_id)
    
    return render(request, 'cursos/confirmar_eliminar_clase.html', {
        'clase': clase,
        'modulo': clase.modulo,
        'curso': clase.modulo.curso
    })

@login_required
def crear_resena(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    inscripcion = Inscripcion.objects.filter(usuario=request.user, curso=curso).first()
    if not inscripcion:
        messages.error(request, 'Debes estar inscripto en el curso para dejar una reseña')
        return redirect('detalle_curso', curso_id=curso_id)
    
    resena_existente = Resena.objects.filter(usuario=request.user, curso=curso).first()
    
    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena_existente)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.usuario = request.user
            resena.curso = curso
            resena.save()
            messages.success(request, 'Reseña guardada exitosamente')
            return redirect('detalle_curso', curso_id=curso_id)
    else:
        form = ResenaForm(instance=resena_existente)
    
    return render(request, 'cursos/crear_resena.html', {
        'form': form,
        'curso': curso,
        'resena_existente': resena_existente
    })

@login_required
def eliminar_resena(request, resena_id):
    resena = get_object_or_404(Resena, id=resena_id)
    
    if resena.usuario != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta reseña')
        return redirect('detalle_curso', curso_id=resena.curso.id)
    
    curso_id = resena.curso.id
    
    if request.method == 'POST':
        resena.delete()
        messages.success(request, 'Reseña eliminada exitosamente')
        return redirect('detalle_curso', curso_id=curso_id)
    
    return render(request, 'cursos/confirmar_eliminar_resena.html', {
        'resena': resena,
        'curso': resena.curso
    })
