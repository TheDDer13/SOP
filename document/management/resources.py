from import_export import resources
from .models import Regulation, Permission
from django.contrib.auth.models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id','username',)

class RegulationResource(resources.ModelResource):
    class Meta:
        model = Regulation
        fields = ('id','name','code','revision','issued_date','issued_by','recall','link','classified')

class PermissionResource(resources.ModelResource):
    class Meta:
        model = Permission
        import_id_fields = ('document_id','user_id',)
        fields = ('document_id','user_id',)