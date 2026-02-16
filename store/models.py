from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    description = models.TextField()    
    brand = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    special_price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    long_description = models.TextField()
    specification = models.TextField()

    def __str__(self):
        return self.name
    
    def get_price(self):
        return self.special_price if self.special_price else self.price        


class StoreSetting(models.Model):
    site_name = models.CharField(max_length=255, default="My Store")
    logo = models.ImageField(upload_to="store/logo/", null=True, blank=True)
    contact_email = models.EmailField(default="inderjeet.singh.1@netsolutions.com")
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10, default="$")
    shipping_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Store Setting"
        verbose_name_plural = "Store Settings"

    def __str__(self):
        return "Store Settings"
    


from decimal import Decimal
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=3, unique=True, help_text="Example: IN, US, UK")

    class Meta:
        verbose_name_plural = "Countries"

    def save(self, *args, **kwargs):
        self.iso_code = self.iso_code.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Carriage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="carriages",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Carriage"
        verbose_name_plural = "Carriages"

    def __str__(self):
        return f"{self.name} ({self.price})"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="payment_methods",
        null=True,
        blank=True
    )
    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    carriage = models.ForeignKey(Carriage, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)    
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
