from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        fields = UserCreationForm.Meta.fields + ('nombre', 'apellido','email', 'telefono')