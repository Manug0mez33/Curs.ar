from datetime import datetime

def bienvenido(request):
    hora_actual = datetime.now().hour
    if request.user.is_authenticated:
        nombre_usuario = request.user.nombre or request.user.first_name or request.user.username      
        if 5 <= hora_actual < 12:
            saludo = f"¡Buenos días {nombre_usuario}!"
        elif 12 <= hora_actual < 18:
            saludo = f"¡Buenas tardes {nombre_usuario}!"
        else:
            saludo = f"¡Buenas noches {nombre_usuario}!"
    else:
        if 5 <= hora_actual < 12:
            saludo = "¡Buenos días!"
        elif 12 <= hora_actual < 18:
            saludo = "¡Buenas tardes!"
        else:
            saludo = "¡Buenas noches!"
    return {'saludo_bienvenida': saludo}