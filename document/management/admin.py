from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Regulation, Permission
from .resources import RegulationResource, PermissionResource, UserResource

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

class RegulationAdmin(ImportExportModelAdmin):
    resource_class = RegulationResource

class PermissionAdmin(ImportExportModelAdmin):
    resource_class = PermissionResource

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Regulation,RegulationAdmin)
admin.site.register(Permission,PermissionAdmin)
