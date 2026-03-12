from django.db import models
from shop.models import Product

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.event_name

class PickupSlot(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='pickup_slots')
    pickup_time = models.TimeField()
    location = models.CharField(max_length=200)
    max_orders = models.IntegerField()
    current_orders = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.event.event_name} - {self.pickup_time}"

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    pickup_slot = models.ForeignKey(PickupSlot, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderItem {self.id}'

    def get_cost(self):
        return self.price * self.quantity
