from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Regulation, QA, QC
from .resources import RegulationResource, QAResource, QCResource

class RegulationAdmin(ImportExportModelAdmin):
    resource_class = RegulationResource

class QAAdmin(ImportExportModelAdmin):
    resource_class = QAResource

class QCAdmin(ImportExportModelAdmin):
    resource_class = QCResource

# Register your models here.
admin.site.register(Regulation,RegulationAdmin)
admin.site.register(QA,QAAdmin)
admin.site.register(QC,QCAdmin)