from django.contrib import admin

# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *

# @admin.register(Shop)
# class ShopAdmin(OSMGeoAdmin):
#     list_display = ('name', 'location')

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShareItem)
admin.site.register(Share)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(SellerProfile)
admin.site.register(PhoneOTP)

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'city', 'phone', 'website','name')

    def user_info(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone', 'user')
        return queryset

    user_info.short_description = 'Info'

admin.site.register(UserProfile, UserProfileAdmin)