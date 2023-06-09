from django.utils import timezone

from authorization.models import (
    CustomUser, OutputProfit
)


def get_count_new_requests_for_output():
    return OutputProfit.objects.filter(is_confirmed=False).count()


def get_outputs_profit(user: CustomUser):
    return OutputProfit.objects.filter(user=user, is_confirmed=True).order_by(
        '-datetime_output'
    ).values('output_sum', 'datetime_output')


def _is_user_can_make_output_request_profit(user: CustomUser) -> bool:
    diff = timezone.now() - user.last_output
    return diff > timezone.timedelta(days=30)


def try_make_output_request_profit(user: CustomUser):
    if _is_user_can_make_output_request_profit(user):
        now_datetime = timezone.datetime.now()
        instance_output = OutputProfit(
            output_sum=user.current_income, datetime_output=now_datetime, user=user
        )
        user.last_output = now_datetime
        user.save()
        instance_output.save()
