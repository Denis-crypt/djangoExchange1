from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    balance = models.FloatField("баланс", default=0)
    last_output = models.DateTimeField(
        'последний вывод',
        default=timezone.datetime.fromtimestamp(0)
    )
    binance_api_key = models.CharField('Binance API Key', max_length=200)
    binance_api_secret = models.CharField('Binance API Secret', max_length=200)
    trades_update_datetime = models.DateTimeField('подтягивать сделки с', default=timezone.datetime.now)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class OutputProfit(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=False, verbose_name='пользователь')
    output_sum = models.FloatField("сумма вывода")
    datetime_output = models.DateTimeField("дата вывода")
    is_confirmed = models.BooleanField("подтверждено", default=False)

    class Meta:
        verbose_name = "вывод прибыли"
        verbose_name_plural = "операции вывода прибыли"
