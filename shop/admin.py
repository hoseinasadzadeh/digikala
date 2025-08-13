from django.contrib import admin
from . import models
from django.contrib.auth.models import User

admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.Category)
admin.site.register(models.Profile)

class ProfileInline(admin.StackedInline):
    model = models.Profile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
    
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)