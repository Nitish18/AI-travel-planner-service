
from django.db import models
from multiselectfield import MultiSelectField

from karo_travel_plan.constants import (TRAVELLING_WITH_CHOICES, TRAVELLING_STYLE_CHOICES, FOOD_PREF_CHOICES,
                                        ACCOMODATION_PREF_CHOICES)
from karo_auth.models import Customer


class TravelPlanQuery(models.Model):
    id = models.UUIDField(db_index=True, unique=True, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    no_of_days = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    month = models.CharField(max_length=20, blank=True, null=True)
    food_pref = models.CharField(max_length=100, blank=True, null=True, choices=FOOD_PREF_CHOICES)
    accomodation_pref = models.CharField(max_length=100, blank=True, null=True, choices=ACCOMODATION_PREF_CHOICES)
    travelling_with_pref = models.CharField(choices=TRAVELLING_WITH_CHOICES, max_length=25, null=True, blank=True)
    travelling_style_pref = MultiSelectField(choices=TRAVELLING_STYLE_CHOICES, null=True, blank=True, max_length=200)
    custom_requirements = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Travel Plan Query"
        verbose_name_plural = "Travel Plan Queries"

    def __str__(self):
        return (f"City: {self.city}, Country: {self.country}, "
                f"Customer: {self.customer.user.email}")


class TravelPlanQueryResponse(models.Model):
    id = models.UUIDField(db_index=True, unique=True, primary_key=True)
    travel_plan_query = models.ForeignKey(TravelPlanQuery, on_delete=models.CASCADE)
    query_response_data = models.JSONField()
    upvote_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Travel Plan Query Response"
        verbose_name_plural = "Travel Plan Query Responses"

    def __str__(self):
        return (f"City: {self.travel_plan_query.city}, Country: {self.travel_plan_query.country}, "
                f"Customer: {self.travel_plan_query.customer.user.email}")


class TravelCity(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    city = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Travel City"
        verbose_name_plural = "Travel Cities"

    def __str__(self):
        return self.city
