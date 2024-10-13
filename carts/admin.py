from typing import LiteralString
from django.contrib import admin

from carts.models import Cart


# admin.site.register(Cart)

class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = 'product', 'quantity', 'created_timestamp'
    search_fields = 'product', 'quantity', 'created_timestamp'
    readonly_fields = ('created_timestamp',)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'product_display', 'quantity', 'created_timestamp']
    list_filter = ['created_timestamp', 'user', 'product__name']

    def user_display(self, object) -> str | LiteralString:
        if object.user:
            return str(object.user)
        else:
            return f"Анонимный пользователь"

    def product_display(self, object) -> str:
        return str(object.product.name)
        
    
    user_display.short_description = "Пользователь"
    product_display.short_description = "Товар"


