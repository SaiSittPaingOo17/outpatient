from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Doctor, Department

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'dep_name', 'dep_email', 'dep_phone', 'dep_location', 'description', 'status')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'lname', 'department', 'specialisation', 'email', 'phone', 'address', 'status')

    def save_model(self, request, obj, form, change):
        # Hash password if it is changed and not already hashed
        if obj.password and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Department, DepartmentAdmin)
