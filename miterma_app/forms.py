from django import forms
from .models import Usuario, Rol

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'id': 'modal-email',
        'placeholder': 'Ingresa tu email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'id': 'modal-password',
        'placeholder': 'Ingresa tu contraseña'
    }))

class RegistroForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'placeholder': 'Ingresa tu email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'placeholder': 'Crea una contraseña'
    }))
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'placeholder': 'Confirma tu contraseña'
    }))
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'placeholder': 'Tu nombre'
    }))
    apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'placeholder': 'Tu apellido'
    }))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent',
        'placeholder': 'Tu teléfono (opcional)'
    }))
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")
        email = cleaned_data.get("email")
        
        # Validar que las contraseñas coincidan
        if password and confirmar_password:
            if password != confirmar_password:
                raise forms.ValidationError("Las contraseñas no coinciden")
        
        # Validar que el email no esté registrado
        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado")
        
        return cleaned_data
