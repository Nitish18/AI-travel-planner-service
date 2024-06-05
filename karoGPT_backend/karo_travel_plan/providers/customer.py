import logging

from karo_auth.models import Customer

logger = logging.getLogger(__name__)


def get_customer_from_id(customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        return customer
    except Customer.DoesNotExist:
        logger.error(f"Customer with id {customer_id} does not exist")
        return None
