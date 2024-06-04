from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Employee)
admin.site.register(Building)
admin.site.register(RentalSpace)
admin.site.register(SpaceStatus)
admin.site.register(Tenant)
admin.site.register(MaintenanceBill)
admin.site.register(RentalAgreement)
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(PaymentCategory)