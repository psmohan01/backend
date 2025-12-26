from django.db import models

class CareerApplication(models.Model):
    POSITION_CHOICES = [
        ('Frontend Developer', 'Frontend Developer'),
        ('Backend Developer', 'Backend Developer'),
        ('UI/UX Designer', 'UI/UX Designer'),
        ('Product Manager', 'Product Manager'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    message = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.position}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

