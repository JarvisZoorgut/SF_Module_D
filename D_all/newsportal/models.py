from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import reverse
from django.core.cache import cache


class Author(models.Model):
    authorUser = models.ForeignKey(User, on_delete=models.CASCADE)
    
    ratingAuthor = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.authorUser} / Рейтинг: {self.ratingAuthor}'

    def uptate_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat = postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')

    CATEGORY_CHOICES = (
        ('NW', 'Новость'),
        ('AR', 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержание')
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'

    def __str__(self):
        return f'{self.categoryType} / {self.title}'    
    
    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        return f'{self.text[:123]}... / Рейтинг: {self.rating}'
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь Пост/Категория'
        verbose_name_plural = 'Связи Пост/Категория'

    def __str__(self):
        return f'{self.postThrough.title} / {self.categoryThrough.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

class Subscriber(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscribers',)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscribers',)

    def __str__(self):
        return f'{self.user} подписан на {self.category}'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['user']