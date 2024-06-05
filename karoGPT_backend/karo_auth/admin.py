
from django.contrib import admin

from karo_auth.models import Plan, Customer, CustomerMetaInfo


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'credit', 'gpt_service_type_config', 'is_active')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'credit_remaining')
    search_fields = ('user__email', )


class CustomerMetaInfoAdmin(admin.ModelAdmin):
    list_display = ('customer', 'digital_travel_user_id', 'digital_travel_user_email')
    search_fields = ('customer__user__email', )


admin.site.register(Plan, PlanAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerMetaInfo, CustomerMetaInfoAdmin)
