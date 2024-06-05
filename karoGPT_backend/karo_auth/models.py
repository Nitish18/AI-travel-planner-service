
from django.contrib.auth.models import User
from django.db import models

from gpt_query_client.models import GPTServiceTypeConfig
from karo_auth.constants import PLAN_TYPE_CHOICES


class Plan(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(choices=PLAN_TYPE_CHOICES, max_length=25)
    credit = models.PositiveIntegerField(default=10)
    gpt_service_type_config = models.ForeignKey(GPTServiceTypeConfig, on_delete=models.deletion.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"


class Customer(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, related_name='customers', on_delete=models.deletion.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.deletion.DO_NOTHING)
    credit_remaining = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class CustomerMetaInfo(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.deletion.CASCADE)
    digital_travel_user_id = models.IntegerField(blank=True, null=True)
    digital_travel_user_email = models.EmailField(blank=True, null=True)
