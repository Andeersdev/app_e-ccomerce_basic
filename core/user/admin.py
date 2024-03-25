from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, object, form, change):
        if object.password.startswith('pbkdf2'):
            object.password = object.password
        else:
            object.set_password(object.password)
        super().save_model(request, object, form, change)


admin.site.register(User, UserAdmin)
