# Em biblioteca/admin.py
from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'editora', 'ano', 'categoria']  # Campos a exibir na lista
    search_fields = ['titulo', 'autor', 'editora', 'ano', 'categoria'] # Campos de pesquisa
    list_filter = ['titulo', 'autor', 'editora', 'ano', 'categoria']  # Filtros laterais