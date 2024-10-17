import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Note, Category
from .factories import UserFactory, CategoryFactory, NoteFactory


@pytest.mark.django_db
class TestNoteAPI:
    @pytest.fixture
    def api_client(self):
        """Fixture para criar uma instância do APIClient."""
        return APIClient()

    @pytest.fixture(scope='session')
    def user(self):
        """Fixture para criar um usuário autenticado."""
        return UserFactory()

    def test_list_notes(self, api_client, user):
        """Testa o endpoint de listagem de notas."""
        NoteFactory.create_batch(3, owner=user)  # Cria 3 notas para o usuário
        api_client.force_authenticate(user=user)  # Autentica o usuário
        url = reverse("note-list")  # Endpoint de listagem de notas
        response = api_client.get(url)  # Faz a requisição GET
        assert response.status_code == 200  # Verifica se a resposta é 200 OK
        assert (
            len(response.data) == 3
        )  # Verifica se a quantidade de notas na resposta é 3

    # @pytest.mark.parametrize(api_client, user)
    def test_create_note(self, api_client, user):
        """Testa o endpoint de criação de uma nova nota."""
        api_client.force_authenticate(user=user)  # Autentica o usuário
        url = reverse("note-list")  # Endpoint de criação de notas
        data = {
            "title": "Test Note",
            "content": "This is a test note",
            "category_names": ["Test Category"],
        }
        response = api_client.post(url, data, format="json")  # Faz a requisição POST

        assert response.status_code == 201  # Verifica se a resposta é 201 Created
        assert Note.objects.count() == 1  # Verifica se uma nova nota foi criada
        assert Category.objects.count() == 1  # Verifica se a categoria foi criada

    def test_create_note_unauthenticated(self, api_client):
        """Testa o endpoint de criação de nota para um usuário não autenticado."""
        url = reverse("note-list")  # Endpoint de criação de notas
        data = {
            "title": "Test Note",
            "content": "This is a test note",
            "category_names": ["Test Category"],
        }
        response = api_client.post(url, data, format="json")  # Faz a requisição POST

        assert response.status_code == 403  # Verifica se a resposta é 403 Forbidden

    def test_update_note(self, api_client, user):
        """Testa o endpoint de atualização de uma nota."""
        note = NoteFactory(owner=user)  # Cria uma nota para o usuário
        api_client.force_authenticate(user=user)  # Autentica o usuário
        url = reverse(
            "note-detail", kwargs={"pk": note.id}
        )  # Endpoint de detalhe de uma nota específica
        data = {
            "title": "Updated Note",
            "content": "This note has been updated",
            "category_names": ["New Category"],
        }
        response = api_client.patch(url, data, format="json")  # Faz a requisição PATCH

        assert response.status_code == 200  # Verifica se a resposta é 200 OK
        updated_note = Note.objects.get(id=note.id)  # Busca a nota atualizada
        assert (
            updated_note.title == "Updated Note"
        )  # Verifica se o título foi atualizado
        assert (
            updated_note.categories.count() == 1
        )  # Verifica se a nova categoria foi associada

    def test_update_note_unauthenticated(self, api_client):
        """Testa o endpoint de atualização de nota para um usuário não autenticado."""
        note = NoteFactory()  # Cria uma nota
        url = reverse(
            "note-detail", kwargs={"pk": note.id}
        )  # Endpoint de detalhe de uma nota específica
        data = {
            "title": "Updated Note",
            "content": "This note has been updated",
            "category_names": ["New Category"],
        }
        response = api_client.patch(url, data, format="json")  # Faz a requisição PATCH

        assert response.status_code == 403  # Verifica se a resposta é 403 Forbidden

    def test_delete_note(self, api_client, user):
        """Testa o endpoint de exclusão de uma nota."""
        note = NoteFactory(owner=user)  # Cria uma nota para o usuário
        api_client.force_authenticate(user=user)  # Autentica o usuário
        url = reverse(
            "note-detail", kwargs={"pk": note.id}
        )  # Endpoint de detalhe de uma nota específica
        response = api_client.delete(url)  # Faz a requisição DELETE

        assert response.status_code == 204  # Verifica se a resposta é 204 No Content
        assert Note.objects.count() == 0  # Verifica se a nota foi excluída

    def test_delete_note_unauthenticated(self, api_client):
        """Testa o endpoint de exclusão de nota para um usuário não autenticado."""
        note = NoteFactory()  # Cria uma nota
        url = reverse(
            "note-detail", kwargs={"pk": note.id}
        )  # Endpoint de detalhe de uma nota específica
        response = api_client.delete(url)  # Faz a requisição DELETE

        assert response.status_code == 403  # Verifica se a resposta é 403 Forbidden

    def test_update_nonexistent_note(self, api_client, user):
        """Testa a atualização de uma nota que não existe."""
        api_client.force_authenticate(user=user)  # Autentica o usuário
        url = reverse("note-detail", kwargs={"pk": 9999})  # ID que não existe
        data = {
            "title": "Updated Note",
            "content": "This note has been updated",
            "category_names": ["New Category"],
        }
        response = api_client.patch(url, data, format="json")  # Faz a requisição PATCH

        assert response.status_code == 404  # Verifica se a resposta é 404 Not Found
