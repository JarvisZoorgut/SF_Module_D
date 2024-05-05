from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.core.cache import cache # импортируем наш кэш

from newsportal.models import Author, Post, Category, Subscriber
from django.contrib.auth.models import User
from .tasks import send_notification_email


class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts_count'] = self.filterset.qs.count()
        context['filterset'] = self.filterset
        context['user_is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['user_is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'newsportal/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        
        if obj is None:  # Проверяем явно на None, чтобы не использовать неявное преобразование типов
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        
        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'newsportal/news_create.html'

    def handle_no_permission(self):
        return render(self.request, '403_login.html', status=403) 

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        current_author = self.request.user
        author, created = Author.objects.get_or_create(authorUser=current_author)
        post.author = author
        post.save()

        return super().form_valid(form)

   
class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post')
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'NW':
            raise forms.ValidationError("По этому пути нельзя редактировать СТАТЬИ")
        
        return obj
    

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_post')
    raise_exception = True
    model = Post
    template_name = 'newsportal/post_delete.html'
    success_url = reverse_lazy('posts')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'NW':
            raise forms.ValidationError("По этому пути нельзя удалить СТАТЬИ")
        
        return obj


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    form_class = ArticleForm
    model = Post
    template_name = 'newsportal/article_create.html'

    def handle_no_permission(self):
        return render(self.request, '403_login.html', status=403)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        current_author = self.request.user
        author, created = Author.objects.get_or_create(authorUser=current_author)
        post.author = author
        return super().form_valid(form)


class ArticlesEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post')
    raise_exception = True
    form_class = ArticleForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'AR':
            raise forms.ValidationError("По этому пути нельзя редактировать НОВОСТИ")
        
        return obj


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_post')
    raise_exception = True
    model = Post
    template_name = 'newsportal/post_delete.html'
    success_url = reverse_lazy('posts')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'AR':
            raise forms.ValidationError("По этому пути нельзя удалить НОВОСТИ")
        
        return obj


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user=request.user, category=category,).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(user=request.user, category=OuterRef('pk'),)
        )
    ).order_by('name')
    return render(request, 'store/templates/store/subscriptions.html', {'categories': categories_with_subscriptions},)
