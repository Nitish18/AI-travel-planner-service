
from django.db import models

from gpt_query_client.constants import GPT_SERVICE_CHOICES


class GPTServiceTypeConfig(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    gpt_service = models.CharField(choices=GPT_SERVICE_CHOICES, max_length=25)
    gpt_model_name = models.CharField(max_length=50)
    max_tokens = models.IntegerField()
    model_temperature = models.FloatField()
    top_p = models.FloatField()
    frequency_penalty = models.FloatField()

    class Meta:
        verbose_name = "GPT Service Type Config"
        verbose_name_plural = "GPT Service Type Configs"
