from django.contrib import admin
from .models import Category, Product, Order, OrderItem# Remove or comment out Favorite

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Favorite)  # Remove or comment out this line
