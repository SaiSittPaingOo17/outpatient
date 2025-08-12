from django.db import models
from accounts.models import User
from doctor.models import Department 

class Nurse(models.Model):

    GENDER_CHOICE = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ]

    STATUS_CHOICE = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    department = models.ForeignKey(Department, on_delete= models.CASCADE, related_name='nurses')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE)
    date_of_birth = models.DateField()
    license = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nurse'
        verbose_name_plural = 'Nurses'

    def __str__(self):
        return f'{self.fname} {self.lname}'