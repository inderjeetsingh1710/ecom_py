# from django.contrib import admin
# from .models import Product, Category, StoreSetting, Order, OrderItem

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(StoreSetting)

# class StoreSettingAdmin(admin.ModelAdmin):
#     list_display = ("site_name", "contact_email", "currency", "shipping_charge")

# Register your models here
from django.contrib import admin
from .models import Product, Category, StoreSetting, Order, OrderItem, Carriage, Country, PaymentMethod


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")  # removed 'stock'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(StoreSetting)
class StoreSettingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "currency", "shipping_charge")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "subtotal")

    def subtotal(self, obj):
        if obj.price is None or obj.quantity is None:
            return 0
        return obj.price * obj.quantity


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "email", "total", "created_at")
    list_filter = ("created_at", "city", "state")
    search_fields = ("customer_name", "email", "address", "city", "state", "zip_code")
    readonly_fields = ("subtotal", "shipping_charge", "total", "created_at")

    inlines = [OrderItemInline]


@admin.register(Carriage)
class CarriageAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "country", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code", "country", "description")

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_code")
    search_fields = ("name", "iso_code")

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "country", "is_active", "description")
    list_filter = ("is_active",)
    search_fields = ("name", "code", "country", "description")
