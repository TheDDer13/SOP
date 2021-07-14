from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin
from .models import Classification, SOP
from .resources import ClassificationResource, SOPResource

# class UserAdmin(ImportExportModelAdmin):
#     resource_class = UserResource

class ClassificationAdmin(ImportExportModelAdmin):
    resource_class = ClassificationResource

class SOPAdmin(ImportExportModelAdmin):
    resource_class = SOPResource

# Register your models here.
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Classification,ClassificationAdmin)
admin.site.register(SOP,SOPAdmin)
