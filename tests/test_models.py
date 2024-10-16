import pytest
from core.models import Note, Category
from .factories import UserFactory, CategoryFactory, NoteFactory


@pytest.mark.django_db
class TestNoteModel:
    def test_create_note(self):
        """Testa a criação básica de uma nota."""
        note = NoteFactory()
        assert Note.objects.count() == 1
        assert isinstance(note.title, str)
        assert isinstance(note.content, str)
        assert note.owner is not None

    def test_update_note(self):
        """Testa a atualização de uma nota existente."""
        note = NoteFactory()
        new_title = "Updated Title"
        note.title = new_title
        note.save()
        updated_note = Note.objects.get(id=note.id)
        assert updated_note.title == new_title

    def test_delete_note(self):
        """Testa a exclusão de uma nota."""
        note = NoteFactory()
        note_id = note.id
        note.delete()
        with pytest.raises(Note.DoesNotExist):
            Note.objects.get(id=note_id)

    def test_note_with_categories(self):
        """Testa a criação de uma nota com múltiplas categorias."""
        categories = CategoryFactory.create_batch(3)
        note = NoteFactory(categories=categories)
        assert note.categories.count() == 3

    def test_note_str_method(self):
        """Testa o método __str__ do modelo Note."""
        note = NoteFactory(title="Test Title")
        assert str(note) == "Test Title"

    def test_note_required_fields(self):
        """Testa se os campos obrigatórios da nota são validados corretamente."""
        with pytest.raises(Exception):
            # O campo 'title' e 'owner' são obrigatórios, então tentar criar uma nota sem eles deve falhar
            Note.objects.create(content="Missing title and owner")


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        """Testa a criação básica de uma categoria."""
        category = CategoryFactory()
        assert Category.objects.count() == 1
        assert isinstance(category.name, str)

    def test_update_category(self):
        """Testa a atualização de uma categoria existente."""
        category = CategoryFactory()
        new_name = "Updated Category"
        category.name = new_name
        category.save()
        updated_category = Category.objects.get(id=category.id)
        assert updated_category.name == new_name

    def test_delete_category(self):
        """Testa a exclusão de uma categoria."""
        category = CategoryFactory()
        category_id = category.id
        category.delete()
        with pytest.raises(Category.DoesNotExist):
            Category.objects.get(id=category_id)

    def test_category_str_method(self):
        """Testa o método __str__ do modelo Category."""
        category = CategoryFactory(name="Test Category")
        assert str(category) == "Test Category"
