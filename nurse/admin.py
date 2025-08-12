from django.contrib import admin
from .models import Nurse

class NurseAdmin(admin.ModelAdmin):
    list_display = ('id','fname','lname','gender','date_of_birth','email','phone','address','status')

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Nurse

# hash and save password
class NurseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.password and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Nurse, NurseAdmin)
