from django.contrib import admin
from .models import Nurse

class NurseAdmin(admin.ModelAdmin):
    list_display = ('id','fname','lname','gender','date_of_birth','email','phone','address','status')

admin.site.register(Nurse)
