from django.db import models
from django.db.models.functions import Now
from datetime import date


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('M', 'Married'),
        ('U', 'Unmarried'),
        ('P', 'Prefer not to say'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=64)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    @property
    def age(self):
        """Calculate current age from date of birth"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def soft_delete(self):
        """Soft delete the patient by setting status to inactive"""
        self.status = 'inactive'
        self.save()
    
    def activate(self):
        """Reactivate the patient"""
        self.status = 'active'
        self.save()