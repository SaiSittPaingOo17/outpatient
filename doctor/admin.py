from django.contrib import admin
from .models import Doctor, Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','dep_name', 'dep_email', 'dep_phone', 'dep_location', 'description', 'status')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id','fname','lname','department','license','specialisation','email','phone','address','status')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Department, DepartmentAdmin)
