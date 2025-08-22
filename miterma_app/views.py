from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, RegistroForm
from .models import Usuario, Rol

def index(request):
    # Crear el formulario de login para el modal
    form = LoginForm()
    return render(request, 'index.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']    
            # Validar contra la base de datos con hash
            try:
                usuario = Usuario.objects.get(email=email)
                if check_password(password, usuario.password):
                    return redirect('index')  
                else:
                    form.add_error(None, "Email o contraseña incorrectos")
            except Usuario.DoesNotExist:
                form.add_error(None, "Email o contraseña incorrectos")
    else:
        form = LoginForm()
    
    return render(request, 'base.html', {'form': form})

def registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            telefono = form.cleaned_data.get('telefono')
            #hashear la contraseña
            password_hasheada = make_password(password)
            
            try:
                #asignar el rol id 1 que es el de cliente
                rol_cliente = Rol.objects.get(id=1)  
            except Rol.DoesNotExist:
                form.add_error(None, "Error de configuración: rol cliente no encontrado. Contacte al administrador.")
                return render(request, 'registro.html', {'form': form})
            
            # Crear el usuario con contraseña hasheada
            usuario = Usuario.objects.create(
                email=email,
                password=password_hasheada,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                rol=rol_cliente
            )
            
            # Redirigir al login después del registro exitoso
            return redirect('index')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

