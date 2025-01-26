from django import forms
from django.contrib.auth.forms import UserCreationForm
from Biblioteca_digital.models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'telefono', 'direccion')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Establecemos el rol como 'admin' para los superusuarios
        if user.is_superuser:
            user.role = 'admin'
        if commit:
            user.save()
        return user
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-text'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-textarea'}),
        }

class LibroForm(forms.ModelForm):
    # Cambiar 'categoria' por ModelMultipleChoiceField
    categoria = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),  # Obtenemos todas las categorías
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'input-checkbox'}),  # Casillas de verificación
        required=True  # Requerir que se seleccione al menos una categoría
    )

    class Meta:
        model = Libro
        fields = ['imagen', 'titulo', 'autor', 'isbn', 'fecha_creacion', 'descripcion', 'categoria', 'url_recurso']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'input-file'}),
            'titulo': forms.TextInput(attrs={'class': 'input-text'}),
            'autor': forms.TextInput(attrs={'class': 'input-text'}),
            'isbn': forms.TextInput(attrs={'class': 'input-text'}),
            'fecha_creacion': forms.DateInput(attrs={'type': 'date', 'class': 'input-text'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-textarea'}),
            'url_recurso': forms.URLInput(attrs={'class': 'input-text', 'placeholder': 'URL del recurso'}),
        }
class VistaLibroForm(forms.ModelForm):
    class Meta:
        model = VistaLibro
        fields = ['libro', 'lector']
        widgets = {
            'libro': forms.Select(attrs={'class': 'input-select'}),
            'lector': forms.Select(attrs={'class': 'input-select'}),
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamos
        fields = ['libro', 'lector', 'fecha_devolucion']
        widgets = {
            'libro': forms.Select(attrs={'class': 'input-select'}),
            'lector': forms.Select(attrs={'class': 'input-select'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date', 'class': 'input-text'}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['libro', 'lector', 'estado']
        widgets = {
            'libro': forms.Select(attrs={'class': 'input-select'}),
            'lector': forms.Select(attrs={'class': 'input-select'}),
            'estado': forms.Select(attrs={'class': 'input-select'}),
        }

class MultaForm(forms.ModelForm):
    class Meta:
        model = Multa
        fields = ['prestamo', 'monto']
        widgets = {
            'prestamo': forms.Select(attrs={'class': 'input-select'}),
            'monto': forms.NumberInput(attrs={'class': 'input-number'}),
        }

class RecomendacionForm(forms.ModelForm):
    class Meta:
        model = Recomendacion
        fields = ['lector', 'libro']
        widgets = {
            'lector': forms.Select(attrs={'class': 'input-select'}),
            'libro': forms.Select(attrs={'class': 'input-select'}),
        }
