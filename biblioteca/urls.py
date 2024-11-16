from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.pagina_inicial, name="pagina_inicial"),
    path("buscar/", views.buscar, name="buscar_livros"),
    path("adicionar-livro/", views.adicionar_livro, name="adicionar_livro"),
    path("editar-livro/<int:pk>/", views.editar_livro, name="editar_livro"),
    path("deletar-livro/<int:pk>/", views.deletar_livro, name="deletar_livro"),
    re_path(r'^api/categoria/(?P<categoria>.+)/$', views.livros_por_categoria, name='livros_por_categoria'),
    path('api/livros/autor/<path:autor_nome>/', views.livros_por_autor, name='livros_por_autor'),
    path('sugestoes/', views.sugestoes, name='sugestoes'),
]
