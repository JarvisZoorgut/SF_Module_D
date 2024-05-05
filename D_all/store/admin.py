from django.contrib import admin
from .models import Category, Product, Subscription


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subscription)