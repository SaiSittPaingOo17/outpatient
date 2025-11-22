from django.contrib import admin
from .models import Pharmacist
from django.contrib.auth.hashers import make_password


class PharmacistAdmin(admin.ModelAdmin):
    list_display = ('id','fname','lname','gender','date_of_birth','email','phone','address','status')

# hash and save password
class PharmacistAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.password and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Pharmacist, PharmacistAdmin)
