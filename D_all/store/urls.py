from django.urls import path
# Импортируем созданные нами представления
from .views import ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, subscriptions, IndexView, create_product

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('products/', ProductsList.as_view(), name = 'products'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('products/<int:pk>', ProductDetail.as_view(), name = 'product_detail'),
    path('products/create/', ProductCreate.as_view(), name = 'product_create'),
    path('products/<int:pk>/update/', ProductUpdate.as_view(), name = 'product_update'),
    path('products/<int:pk>/delete/', ProductDelete.as_view(), name = 'product_delete'),
    path('products/subscriptions/', subscriptions, name='subscriptions',),
    path('', IndexView.as_view()),
    # path('products/create_product/', create_product, name='create_product'), #через def
]