from rest_framework import serializers
from core.models import Note, Category
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializa todos os campos do modelo Category.
    """

    class Meta:
        model = Category
        fields = ["id", "name"]


class NoteSerializer(serializers.ModelSerializer):
    """
    Inclui campos personalizados para o proprietário (somente leitura) e
    para o nome da categoria, além de uma representação personalizada
    para exibir o nome da categoria
    """

    owner = serializers.StringRelatedField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "owner",
            "categories",
            "category_names",
        ]

    def validate_category_data(self, value):
        """
        Valida se cada item em category_data é uma string ou um inteiro.
        """
        if not all(isinstance(item, (str, int)) for item in value):
            raise serializers.ValidationError(
                "Each category must be either a string (name) or an integer (ID)."
            )
        return 

    def create(self, validated_data):
        """
        Cria uma nova nota com as categorias associadas.
        """
        # Extrai os dados de categoria do validated_data
        category_names = validated_data.pop("category_names", [])
        # Define o proprietário como o usuário atual
        validated_data["owner"] = self.context["request"].user

        # Usa uma transação para garantir a integridade dos dados
        with transaction.atomic():
            # Cria a nota
            note = Note.objects.create(**validated_data)
            # Associa as categorias à nota
            self._set_categories(note, category_names)

        return note

    def update(self, instance, validated_data):
        """
        Atualiza uma nota existente, incluindo suas categorias se fornecidas.
        """
        # Extrai os dados de categoria do validated_data
        category_names = validated_data.pop("category_names", None)
        # Atualiza os outros campos da nota
        instance = super().update(instance, validated_data)

        # Se foram fornecidos dados de categoria, atualiza as categorias
        if category_names is not None:
            self._set_categories(instance, category_names)
        return instance

    def _set_categories(self, note, category_names):
        """
        Associa categorias a uma nota, criando novas se necessário.
        """
        categories = []
        for item in category_names:
            if isinstance(item, int):
                # Se o item é um ID, tenta obter a categoria existente
                try:
                    category = Category.objects.get(id=item)
                    categories.append(category)
                except Category.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Category with id {item} does not exist."
                    )
            else:
                # Se o item é uma string, normaliza o nome e obtém ou cria a categoria
                normalized_name = self._normalize_category_name(item)
                category, created = Category.objects.get_or_create(name=normalized_name)
                categories.append(category)

        # Define as categorias da nota
        note.categories.set(categories)

    def _normalize_category_name(self, name):
        """
        Normaliza o nome da categoria: converte para minúsculas e remove espaços extras.
        """
        return " ".join(name.lower().split())

    @transaction.atomic
    def _optimize_category_query(self, category_names):
        """
        Otimiza a criação e recuperação de categorias em lote.
        """
        # Converte todos os nomes para a forma normalizada
        normalized_names = [
            self._normalize_category_name(item)
            for item in category_names
            if isinstance(item, str)
        ]

        # Busca todas as categorias existentes em uma única consulta
        existing_categories = {
            cat.name: cat for cat in Category.objects.filter(name__in=normalized_names)
        }

        # Cria quaisquer categorias ausentes em lote
        new_categories = [
            Category(name=name)
            for name in normalized_names
            if name not in existing_categories
        ]
        Category.objects.bulk_create(new_categories)

        # Combina categorias existentes e novas
        all_categories = list(existing_categories.values()) + new_categories

        return all_categories
