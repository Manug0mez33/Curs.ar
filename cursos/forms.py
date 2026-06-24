from django import forms
from .models import Curso, Modulo, Clase

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
            'titulo', 
            'descripcion',
            'categoria',
            'precio',
            'duracion',
            'imagen'
        ]
        error_messages = {
            'required': 'Este campo es obligatorio.',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Introducción a Python',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el contenido del curso',
                'required': True
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Ej: 5000',
                'required': True
            }),
            'duracion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ej: 40',
                'required': True
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio
    
    def clean_duracion(self):
        duracion = self.cleaned_data.get('duracion')
        if duracion is not None and duracion < 1:
            raise forms.ValidationError('La duración debe ser al menos 1 hora.')
        return duracion

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['titulo', 'descripcion', 'orden']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Módulo 1 - Conceptos Básicos',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el contenido del módulo',
                'required': True
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ej: 1',
                'required': True
            })
        }

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['titulo', 'contenido', 'orden']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Instalación del entorno',
                'required': True
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Contenido de la clase',
                'required': True
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ej: 1',
                'required': True
            })
        }
    
