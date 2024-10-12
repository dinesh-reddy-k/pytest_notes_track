from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Note, Category
from .serializers import NoteSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Fornece operações CRUD para categorias.
    Requer autenticação para todas as operações.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class NoteViewSet(viewsets.ModelViewSet):
    """
    Fornece operações CRUD para as anotações.
    Filtra as notas para mostrar apenas as do usuário atual.
    Requer autenticação para todas as operações.
    """

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna um queryset de notas filtrado para incluir apenas
        as notas do usuário atual.
        """
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Sobrescreve o método perform_create para definir o proprietário
        da nota como o usuário atual antes de salvar.
        """
        serializer.save(owner=self.request.user)
