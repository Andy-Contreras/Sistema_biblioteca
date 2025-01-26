from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Categoria, Libro
# Create your views here.
def home(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    libros_recomendados = Libro.objects.filter(recomendacion__isnull=False).distinct()  # Libros que tienen al menos una recomendación

    # Mostrar los primeros 5 libros recomendados
    libros_recomendados_limitados = libros_recomendados[:5]

    # Verificar si hay más de 5 libros recomendados
    hay_mas_libros = libros_recomendados.count() >= 5

    return render(request, 'home.html', {
        'categorias': categorias,
        'libros_recomendados': libros_recomendados_limitados,
        'hay_mas_libros': hay_mas_libros
    })
def register_view(request):
    from django.contrib.auth import login
    from .forms import CustomUserCreationForm
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
        else:
            messages.error(request, 'El registro falló. Por favor corrija los errores')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/register.html', {'form': form})

def login_view(request):
    from django.contrib.auth import login, authenticate
    from .forms import LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitosa!')
                return redirect('home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña no validos.')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'Te has desconectado.')
    return redirect('login')

