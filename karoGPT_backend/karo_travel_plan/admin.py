# admin.py
from django.contrib import admin

from .models import TravelCity, TravelPlanQuery, TravelPlanQueryResponse


class TravelPlanQueryAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id', 'no_of_days', 'city', 'country', 'food_pref', 'accomodation_pref',
        'travelling_style_pref', 'custom_requirements', 'is_active',
    )
    search_fields = ('customer__user__email', 'city', 'country')


class TravelPlanQueryResponseAdmin(admin.ModelAdmin):
    list_display = ('travel_plan_query', 'upvote_count', 'is_active', 'created_at')
    search_fields = ('travel_plan_query__customer__user__email', 'travel_plan_query__city',
                     'travel_plan_query__country')


class TravelCityAdmin(admin.ModelAdmin):
    list_display = ('city', 'is_active', 'country')
    search_fields = ('city', 'country')


admin.site.register(TravelPlanQuery, TravelPlanQueryAdmin)
admin.site.register(TravelPlanQueryResponse, TravelPlanQueryResponseAdmin)
admin.site.register(TravelCity, TravelCityAdmin)
