from django import template
from django.utils import timezone

from authorization.services import get_outputs_profit

register = template.Library()


@register.simple_tag
def get_my_realized_pnl(transactions):
    return sum([transaction.realized_pnl for transaction in transactions])


@register.simple_tag
def is_user_can_output_profit(user):
    diff = timezone.now() - user.last_output
    return diff > timezone.timedelta(days=30)


@register.simple_tag
def get_user_output_history(user):
    return get_outputs_profit(user)


@register.simple_tag
def get_user_current_income_plus_balance(user):
    return user.current_income + user.balance
