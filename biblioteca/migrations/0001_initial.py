# Generated by Django 5.1.3 on 2024-11-11 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(blank=True, max_length=255, null=True)),
                ('titulo', models.CharField(blank=True, max_length=255, null=True)),
                ('editora', models.CharField(blank=True, max_length=255, null=True)),
                ('ano', models.CharField(blank=True, max_length=10, null=True)),
                ('categoria', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]