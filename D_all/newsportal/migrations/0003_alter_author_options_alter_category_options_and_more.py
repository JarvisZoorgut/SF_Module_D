# Generated by Django 5.0.2 on 2024-02-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsportal', '0002_alter_author_authoruser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Контент', 'verbose_name_plural': 'Контент'},
        ),
        migrations.AlterModelOptions(
            name='postcategory',
            options={'verbose_name': 'Связь Пост/Категория', 'verbose_name_plural': 'Связи Пост/Категория'},
        ),
        migrations.AlterField(
            model_name='post',
            name='postCategory',
            field=models.ManyToManyField(through='newsportal.PostCategory', to='newsportal.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Заголовок'),
        ),
    ]