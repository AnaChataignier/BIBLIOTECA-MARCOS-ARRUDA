from django.db import models


class Livro(models.Model):
    autor = models.CharField(max_length=255, null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    editora = models.CharField(max_length=255, null=True, blank=True)
    ano = models.CharField(max_length=13, null=True, blank=True)
    categoria = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.titulo


class Tema(models.Model):
    categoria = models.CharField(max_length=255)

    def __str__(self):
        return self.categoria
