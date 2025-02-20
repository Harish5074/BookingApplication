from django.db import models
from django.utils import timezone

# Constants for booking limit and inventory counts
MAX_BOOKINGS = 2

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    booking_count = models.IntegerField(default=0)
    date_joined = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Inventory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    remaining_count = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.title

class Booking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking for {self.member} - {self.inventory.title} on {self.booking_date}"
