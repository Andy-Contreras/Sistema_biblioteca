from django.urls import path
from . import views
from .biblioteca import *

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('visualizar_libro/<int:libro_id>/', visualizar_libro, name='visualizar_libro'),
    path('', views.home, name='home'),
    path('libro_listado/', LibroList.as_view(), name='libro_listado'),
    path('libro_creado/', LibroCreate.as_view(), name='libro_creado'),
    path('libro_editar/<int:pk>/', LibroUpdate.as_view(), name='libro_editar'),
    path('libro_eliminar/<int:pk>/', LibroDelete.as_view(), name='libro_eliminar'),
    path('categoria_listado/', CategoriaList.as_view(), name='categoria_listado'),
    path('categoria_creado/', CategoriaCreate.as_view(), name='categoria_creado'),
    path('categoria_editar/<int:pk>/', CategoriaUpdate.as_view(), name='categoria_editar'),
    path('categoria_libro/<int:categoria_id>/', LibroCategoriaList.as_view(), name='categoria_libro'),
    path('libros_recomendados/', LibroRecomendadoListView.as_view(), name='libros_recomendados'),
    path('recomendar/<int:libro_id>/', Recomendarlibro.as_view(), name='recomendar_libro'),
    path('busqueda/', Busqueda_Libro.as_view(), name='busqueda_libros'),

]