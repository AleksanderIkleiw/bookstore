from django.contrib import admin
from .models import Book, Author, ShoppingCart, Order

"""
In order to be able to view and/or edit models on admin site we have to register them
"""
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(ShoppingCart)
admin.site.register(Order)
