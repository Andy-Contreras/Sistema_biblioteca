from email.policy import default

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.conf import settings
class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('librarian', 'Bibliotecario'),
        ('reader', 'Lector'),
    ]
    nombre = models.CharField(max_length=15, blank=True, null=True)
    apellido = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    perfil_imagen = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='reader')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # NOMBRE ÚNICO
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # NOMBRE ÚNICO
        blank=True,
        help_text='Specific permissions for this user.'
    )
    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == 'admin'

    def is_librarian(self):
        return self.role == 'librarian'

    def is_reader(self):
        return self.role == 'reader'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    imagen = models.ImageField(upload_to='libros/', blank=True, null=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_creacion = models.DateField()
    descripcion = models.TextField()
    categoria = models.ManyToManyField('Categoria')
    vistas_digitales = models.PositiveIntegerField(default=0)
    url_recurso = models.URLField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

    def incrementar_vista(self, lector):
        vista, created = VistaLibro.objects.get_or_create(libro=self, lector=lector)
        if created:
            self.vistas_digitales += 1
            self.save()

class VistaLibro(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    lector = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    fecha_vista = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lector.username} vio {self.libro.titulo} el {self.fecha_vista}"

    class Meta:
        unique_together = ('libro', 'lector')  # Asegura que un lector solo pueda ver un libro una vez.


class Multa(models.Model):
    prestamo = models.OneToOneField('Prestamos', on_delete=models.CASCADE, related_name='multa_relacionada')
    monto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Multa por {self.prestamo.libro.titulo}: {self.monto} USD"

class Prestamos(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    lector = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'reader'})
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField()
    multa = models.OneToOneField('Multa', on_delete=models.CASCADE, related_name='prestamo_relacionado', null=True, blank=True)

    def __str__(self):
        return f"{self.libro.titulo} prestado a {self.lector.username}"


class Reserva(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    lector = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'reader'})
    fecha_reserva = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')], default='pendiente')

    def __str__(self):
        return f"Reserva de {self.libro.titulo} por {self.lector.username}"

class Recomendacion(models.Model):
    lector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_recomendacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Recomendación de {self.libro.titulo} para {self.lector.username}"