from django import forms
from .models import Livro, Tema


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ["autor", "titulo", "editora", "ano", "categoria"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ["categoria"]

