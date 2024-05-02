from django.db import models
from django.contrib.auth.models import User
import os
from django.contrib import admin
from django.utils import timezone

def product_image_path(instance, filename):
    base_name, file_extension = os.path.splitext(filename)
    unique_filename = f"product_{instance.id}{file_extension}"
    return os.path.join('product_images', unique_filename)

# Define the Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_path)

    def __str__(self):
        return self.name


# Extend the User model to include mobile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True)  # Mobile field for UserProfile

    def __str__(self):
        return self.user.username

# Cart model for representing items in the shopping cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relationship with User
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Relationship with Product
    quantity = models.PositiveIntegerField(default=1)  # Default quantity is 1

    def total_price(self):
        return self.quantity * self.product.price  # Calculate total price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Total: {self.total_amount}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"