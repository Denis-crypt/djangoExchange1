from django import template
from django.db.models import QuerySet

from trades_info.models import TradeBinanceUSDT, TradeBinanceCOINM

register = template.Library()


@register.filter
def get_sum_realized_pnl(trade_list: QuerySet[TradeBinanceUSDT, TradeBinanceCOINM]):
    return round(sum([trade_instance.realized_pnl for trade_instance in trade_list]), 2)
