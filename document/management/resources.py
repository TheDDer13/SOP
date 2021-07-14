from import_export import resources
from .models import Classification, SOP
from django.contrib.auth.models import User

class ClassificationResource(resources.ModelResource):
    class Meta:
        model = Classification
        fields = ('classified')
        
class SOPResource(resources.ModelResource):
    class Meta:
        model = SOP
        import_id_fields = ('name','code','revision','issued_date','issued_by','recall','link','dept_classified','sys_classified','permission')
        fields = ('name','code','revision','issued_date','issued_by','recall','link','dept_classified','sys_classified','permission')