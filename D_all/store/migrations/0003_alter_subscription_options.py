# Generated by Django 5.0.2 on 2024-02-15 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_subscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ['user'], 'verbose_name': 'Подписчик', 'verbose_name_plural': 'Подписчики'},
        ),
    ]