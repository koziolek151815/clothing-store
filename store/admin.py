from django.contrib import admin

# Register your models here.
from store.models import Customer, Product, Order, OrderItem

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)