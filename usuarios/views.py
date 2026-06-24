from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from django.contrib.auth import login
from cursos.models import Inscripcion

def registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def perfil(request):
    inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('curso')
    
    datos_perfil = {
        'inscripciones': inscripciones,
        'total_cursos': inscripciones.count()
    }
    
    return render(request, 'perfil/perfil.html', datos_perfil)