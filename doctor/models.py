from django.db import models
from accounts.models import User 

class Department(models.Model):
    STATUS_CHOICE = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    dep_name = models.CharField(max_length=100, unique=True)
    dep_email = models.EmailField(max_length=100)
    dep_phone = models.CharField(max_length=20)
    dep_location = models.TextField(max_length=500)
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"Department of {self.dep_name}"


class Doctor(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="doctors")
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    license = models.CharField(max_length=20, unique=True)
    specialisation = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    password = models.CharField(max_length=128, default='@User123')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f'Dr. {self.fname} {self.lname}'
