from rest_framework import serializers
from core.models import Note, Category
from django.contrib.auth import get_user_model

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
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "owner",
            "category",
            "category_name",
        ]

    def get_category_name(self, obj):
        """Retorna o nome da categoria, se existir."""
        return obj.category.name if obj.category else None

    def to_representation(self, instance):
        """
        Personaliza a representação da nota, substituindo o ID da categoria
        pelo nome da categoria na resposta JSON.
        """
        representation = super().to_representation(instance)
        representation["category"] = representation.pop("category_name")
        return representation

    def create(self, validated_data):
        """
        Sobrescreve o método create para definir o proprietário da nota
        como o usuário atual da requisição.
        """
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
