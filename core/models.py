from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Cada categoria tem um nome único e pode estar associada a várias notas.
    """

    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    """
    Modelo para representar notas individuais.

    Cada nota tem um título, conteúdo, timestamps de criação e atualização,
    uma categoria opcional e um proprietário (usuário que criou a nota).
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name="notes")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
