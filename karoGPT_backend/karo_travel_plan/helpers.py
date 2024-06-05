import logging

logger = logging.getLogger(__name__)


def is_customer_allowed(customer) -> bool:
    customer_plan = customer.plan if customer else None
    if customer_plan is None:
        logger.error("Customer plan not found")
        return False

    if customer_plan.is_active and customer_plan.plan_type == "free":
        return True
    if customer_plan.is_active and customer.credit_remaining > 0:
        return True
    return False
