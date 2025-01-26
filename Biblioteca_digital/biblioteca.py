from django.contrib.auth.decorators import user_passes_test
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from Biblioteca_digital.decorators import no_es_lector
from Biblioteca_digital.forms import *
from Biblioteca_digital.models import *
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
class LibroList(LoginRequiredMixin,ListView):
    model = Libro
    template_name = 'libros/listado_libros.html'
    context_object_name = 'libro_listado'
    def get_queryset(self):
        """Retorna solo libros activos."""
        return Libro.objects.filter(estado=True)


class LibroCreate(LoginRequiredMixin,CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/crear_libros.html'
    success_url = reverse_lazy('libro_listado')

    @method_decorator(user_passes_test(no_es_lector, login_url='home'))  # Aplicamos el decorador aquí
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LibroUpdate(LoginRequiredMixin,UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/crear_libros.html'
    success_url = reverse_lazy('libro_listado')

    def form_valid(self, form):
        libro = form.save()
        return super().form_valid(form)

    @method_decorator(user_passes_test(no_es_lector, login_url='home'))  # Aplicamos el decorador aquí
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LibroDelete(LoginRequiredMixin,DeleteView):
    model = Libro
    template_name = 'libros/eliminar_libros.html'
    success_url = reverse_lazy('libro_listado')

    def post(self, request, pk, *args, **kwargs):
        libro = get_object_or_404(Libro, id=pk)
        libro.estado = False
        libro.save()
        messages.success(request, f"El libro '{libro.titulo}' se ha eliminado lógicamente.")
        return redirect(self.success_url)

    @method_decorator(user_passes_test(no_es_lector, login_url='home'))  # Aplicamos el decorador aquí
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LibroCategoriaList(LoginRequiredMixin,ListView):
    model = Libro
    template_name = 'categorias/libro_categoria.html'
    context_object_name = 'categoria_listado'

    def get_queryset(self):
        categoria_id = self.kwargs.get('categoria_id')  # Obtén el ID de la categoría
        self.categoria = get_object_or_404(Categoria, id=categoria_id)  # Asegúrate de que la categoría exista
        queryset = Libro.objects.filter(categoria=self.categoria, estado=True)  # Filtra libros de la categoría con estado True
        # Lógica de búsqueda
        query = self.request.GET.get('q')  # Toma el término de búsqueda desde la barra de búsqueda
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | Q(autor__icontains=query)  # Busca en título o autor
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria  # Pasa la categoría al contexto
        context['query'] = self.request.GET.get('q', '')  # Pasa el término de búsqueda al contexto
        return context


class CategoriaList(LoginRequiredMixin,ListView):
    model = Categoria
    template_name = 'categorias/categoria_lista.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.annotate(
            libros_count=Count('libro', filter=Q(libro__estado=True))  # Ajusta 'estado' al nombre correcto del campo
        )


class CategoriaCreate(LoginRequiredMixin,CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/crear_categorias.html'
    success_url = reverse_lazy('categoria_listado')

    @method_decorator(user_passes_test(no_es_lector, login_url='home'))  # Aplicamos el decorador aquí
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CategoriaUpdate(LoginRequiredMixin,UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/crear_categorias.html'
    success_url = reverse_lazy('categoria_listado')

    @method_decorator(user_passes_test(no_es_lector, login_url='home'))  # Aplicamos el decorador aquí
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LibroRecomendadoListView(LoginRequiredMixin,ListView):
    model = Recomendacion
    template_name = 'recomendaciones/libro_recomendaciones.html'
    context_object_name = 'libros_recomendados'

    def get_queryset(self):
        # Recuperamos todas las recomendaciones
        return Recomendacion.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Para cada recomendación, obtenemos el libro asociado y el número de recomendaciones
        for recomendacion in context['libros_recomendados']:
            libro = recomendacion.libro  # Obtener el libro relacionado con la recomendación
            # Contamos cuántas veces este libro ha sido recomendado
            recomendacion.num_recomendaciones = Recomendacion.objects.filter(libro=libro).count()

        return context

class Recomendarlibro(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        libro_id = self.kwargs.get('libro_id')  # Obtener el ID del libro desde la URL
        libro = get_object_or_404(Libro, id=libro_id)  # Recuperar el libro por su ID

        if request.user.is_authenticated:  # Verificar que el usuario esté autenticado
            lector = request.user
            # Verificar si ya existe una recomendación para este libro
            if not Recomendacion.objects.filter(lector=lector, libro=libro).exists():
                recomendacion = Recomendacion(lector=lector, libro=libro)
                recomendacion.save()  # Guardamos la recomendación

        # Después de guardar la recomendación, redirigir a la lista de libros
        return redirect('libro_listado')  # O el nombre de la vista donde muestras los libros

def visualizar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)  # Obtiene el libro con el id

    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Si el usuario es un lector, incrementa las vistas
        if request.user.role == 'reader':
            libro.incrementar_vista(request.user)  # Incrementa las vistas

        # Si el libro tiene un enlace de recurso, redirige al recurso
        if libro.url_recurso:
            return redirect(libro.url_recurso)

    # Si no se cumple ninguna condición, redirige a la página de inicio
    return redirect('home')

class Busqueda_Libro(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'libros/busqueda_libros.html'
    context_object_name = 'libro_listado'

    def get_queryset(self):
        """
        Filtra libros según los parámetros ingresados en el formulario de búsqueda avanzada.
        """
        queryset = Libro.objects.filter(estado=True)  # Solo libros activos

        # Capturar los datos de búsqueda desde la URL (GET)
        query = self.request.GET.get('q', '')  # Búsqueda general
        titulo = self.request.GET.get('titulo', '')  # Búsqueda por título
        autor = self.request.GET.get('autor', '')  # Búsqueda por autor
        categoria = self.request.GET.get('categoria', '')  # Búsqueda por categoría

        # Aplicar filtros dinámicamente según los campos llenados
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | Q(autor__icontains=query)
            )
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if autor:
            queryset = queryset.filter(autor__icontains=autor)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Pasar las categorías al contexto para el formulario
        context['query'] = self.request.GET.get('q', '')  # Mantener el valor en la barra de búsqueda general
        context['titulo'] = self.request.GET.get('titulo', '')
        context['autor'] = self.request.GET.get('autor', '')
        context['categoria'] = self.request.GET.get('categoria', '')
        return context





