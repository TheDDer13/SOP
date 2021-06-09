from import_export import resources
from .models import Regulation, QA, QC

class RegulationResource(resources.ModelResource):
    class Meta:
        model = Regulation
        fields = ('name','code','revision','issued_date','issued_by','link',)

class QAResource(resources.ModelResource):
    class Meta:
        model = QA
        fields = ('document','user',)

class QCResource(resources.ModelResource):
    class Meta:
        model = QC
        fields = ('document','user',)