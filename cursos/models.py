from django.db import models
from django.conf import settings

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True)
    precio = models.PositiveIntegerField(default=0, help_text='Precio en pesos')
    duracion = models.PositiveIntegerField(help_text='Duración en horas', default=0)

    def __str__(self):
        return self.titulo
    
class Modulo(models.Model):
    curso = models.ForeignKey(Curso, related_name='modulos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Clase(models.Model):
    modulo = models.ForeignKey(Modulo, related_name='clases', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.modulo.titulo} - {self.titulo}"

class Inscripcion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'curso') 

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo}"

class Resena(models.Model):
    calificaciones = [(i, i) for i in range(1, 6)]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, related_name='resenas', on_delete=models.CASCADE)
    calificacion = models.IntegerField(choices=calificaciones, default=5)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'curso')
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo} ({self.calificacion}⭐)"

