from django.contrib import admin

from gpt_query_client.models import GPTServiceTypeConfig


class GPTServiceTypeConfigAdmin(admin.ModelAdmin):
    list_display = ('gpt_service', 'gpt_model_name', 'max_tokens', 'model_temperature', 'top_p', 'frequency_penalty')
    search_fields = ('gpt_service', 'gpt_model_name', 'max_tokens', 'model_temperature', 'top_p', 'frequency_penalty')


admin.site.register(GPTServiceTypeConfig, GPTServiceTypeConfigAdmin)
