import factory
from factory.django import DjangoModelFactory
from core.models import Note, Category
from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")


class NoteFactory(DjangoModelFactory):
    class Meta:
        model = Note
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=4)
    content = factory.Faker("paragraph")
    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        """
        Este método é chamado após a criação da instância de 'Note'.
        Se 'create' for False, a instância ainda não foi salva no banco de dados,
        então não adicionamos categorias.
        """
        if not create:  # Se a instância não foi salva, não faz nada
            return

        if extracted:  # Se categorias forem passadas, as adiciona
            for category in extracted:
                self.categories.add(category)
