from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from core.models import LinkModel

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'E-Mail:',
            'password': 'Senha:',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder':'Digite seu e-mail institucional'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder':'Digite sua senha'}),
        }
        error_messages = {
            'email': {
                'required': ("Informe o e-mail."),
            },
        }
        


    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@cps.sp.gov.br'):
            raise ValidationError('Informe seu e-mail institucional.')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("Usuário com esse e-mail não encontrado.")

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise ValidationError("Senha incorreta para o e-mail informado.")

            self.user = user
            
class LinkForm(forms.ModelForm):
    class Meta:
        model = LinkModel
        fields = ('titulo', 'link', 'observacao')
        
        labels = {
            'titulo': 'Título do Link:',
            'link': 'Endereço URL:',
            'observacao': 'Observações adicionais:',
        }
        
        # Adição de widgets para estilização com classes do bootstrap
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: Curso gratuito de...'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: https://bluepex.ead...'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Descreva brevemente o destino desse link.'
            }),
        }
    def clean_link(self):
        link = self.cleaned_data.get('link', '').strip()
        if LinkModel.objects.filter(link=link).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este endereço URL já foi cadastrado no sistema.")
        return link