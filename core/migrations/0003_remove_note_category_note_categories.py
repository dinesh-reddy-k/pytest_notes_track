# Generated by Django 5.1.2 on 2024-10-14 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_category_name_alter_note_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="note",
            name="category",
        ),
        migrations.AddField(
            model_name="note",
            name="categories",
            field=models.ManyToManyField(related_name="notes", to="core.category"),
        ),
    ]
