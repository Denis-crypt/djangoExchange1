# Generated by Django 4.0.10 on 2023-06-08 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades_info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradebinancecoinm',
            name='commission',
            field=models.FloatField(default=0, verbose_name='Commission'),
        ),
        migrations.AddField(
            model_name='tradebinancecoinm',
            name='net_profit',
            field=models.FloatField(default=0, verbose_name='Net Profit'),
        ),
        migrations.AddField(
            model_name='tradebinanceusdt',
            name='commission',
            field=models.FloatField(default=0, verbose_name='Commission'),
        ),
        migrations.AddField(
            model_name='tradebinanceusdt',
            name='net_profit',
            field=models.FloatField(default=0, verbose_name='Net Profit'),
        ),
    ]
