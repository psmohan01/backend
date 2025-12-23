from django.db import models
class Booking(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    start_iso = models.CharField(max_length=64)
    end_iso = models.CharField(max_length=64)
    display_time = models.CharField(max_length=64, blank=True)
    google_meet = models.CharField(max_length=512, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} @ {self.start_iso}"
