# Generated by Django 5.0.7 on 2024-07-11 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_rename_consulta_questions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Conversacion',
        ),
    ]
