import logging

logger = logging.getLogger(__name__)


class GPTQueryClient:
    def __init__(self, gpt_service=None, gpt_model_name=None, max_tokens=None, model_temperature=None, top_p=None):
        self.gpt_service = gpt_service
        self.gpt_model_name = gpt_model_name
        self.max_tokens = max_tokens
        self.model_temperature = model_temperature
        self.top_p = top_p

    def _generate_prompt(self, data):
        raise NotImplementedError("Subclasses should implement this method")

    def execute_query(self):
        raise NotImplementedError("Subclasses should implement this method")
