from django.contrib import admin

# Register your models here.

from .models import Transactions,AddShipModel,AddRouteModel,AdduserModel
admin.site.register(Transactions)
admin.site.register(AddShipModel)
admin.site.register(AddRouteModel)
admin.site.register(AdduserModel)
