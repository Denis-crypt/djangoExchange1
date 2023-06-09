from django.db import models
from django.conf import settings


class SymbolBinanceCOINM(models.Model):
    name = models.CharField('Name Symbol', max_length=20)


class PairBinanceCOINM(models.Model):
    name = models.CharField('Name Pair', max_length=10)


class SideBinanceCOINM(models.Model):
    name = models.CharField('Name Side', max_length=20)


class AssetBinanceCOINM(models.Model):
    name = models.CharField('Name Asset', max_length=20)


class PositionSideBinanceCOINM(models.Model):
    name = models.CharField('Name Position Side', max_length=20)


class OrderBinanceCOINM(models.Model):
    binance_id = models.PositiveBigIntegerField('Binance ID')
    order_id = models.PositiveBigIntegerField('Order ID')
    symbol = models.ForeignKey(SymbolBinanceCOINM, on_delete=models.CASCADE, null=False)
    pair = models.ForeignKey(PairBinanceCOINM, on_delete=models.CASCADE, null=False)
    side = models.ForeignKey(SideBinanceCOINM, on_delete=models.CASCADE, null=False)
    price = models.FloatField('Price')
    qty = models.FloatField('qty')
    realized_pnl = models.FloatField('Realized Pnl')
    margin_asset = models.ForeignKey(AssetBinanceCOINM, on_delete=models.CASCADE, null=False,
                                     related_name='orders_margin')
    base_qty = models.FloatField('Base qty')
    commission = models.FloatField('Commission')
    commission_asset = models.ForeignKey(AssetBinanceCOINM, on_delete=models.CASCADE, null=False,
                                         related_name='orders_commission')
    datetime = models.DateTimeField(null=False)
    position_side = models.ForeignKey(PositionSideBinanceCOINM, on_delete=models.CASCADE, null=False)
    maker = models.BooleanField()
    buyer = models.BooleanField()
    trade = models.ForeignKey('TradeBinanceCOINM', on_delete=models.CASCADE, null=True, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)


class TradeBinanceCOINM(models.Model):
    is_close = models.BooleanField('Closed trade')
    symbol = models.ForeignKey(SymbolBinanceCOINM, on_delete=models.CASCADE, null=False)
    position_side = models.ForeignKey(PositionSideBinanceCOINM, on_delete=models.CASCADE, null=False)
    open_datetime = models.DateTimeField('Open datetime')
    close_datetime = models.DateTimeField('Close datetime', null=True)
    open_price = models.FloatField('Open price')
    close_price = models.FloatField('Close price', null=True)
    realized_pnl = models.FloatField('Realized Pnl', default=0)
    commission = models.FloatField('Commission', default=0)
    net_profit = models.FloatField('Net Profit', default=0)
    qty = models.FloatField('Qty')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)


class SymbolBinanceUSDT(models.Model):
    name = models.CharField('Name Symbol', max_length=20)


class SideBinanceUSDT(models.Model):
    name = models.CharField('Name Side', max_length=20)


class PositionSideBinanceUSDT(models.Model):
    name = models.CharField('Name Position Side', max_length=20)


class AssetBinanceUSDT(models.Model):
    name = models.CharField('Name Asset', max_length=20)


class OrderBinanceUSDT(models.Model):
    binance_id = models.PositiveBigIntegerField('Binance ID')
    order_id = models.PositiveBigIntegerField('Order ID')
    symbol = models.ForeignKey(SymbolBinanceUSDT, on_delete=models.CASCADE, null=False)
    side = models.ForeignKey(SideBinanceUSDT, on_delete=models.CASCADE, null=False)
    price = models.FloatField('Price')
    qty = models.FloatField('qty')
    realized_pnl = models.FloatField('Realized Pnl')
    margin_asset = models.ForeignKey(AssetBinanceUSDT, on_delete=models.CASCADE, null=False,
                                     related_name='orders_margin')
    quote_qty = models.FloatField('Quote Qty')
    commission = models.FloatField('Commission')
    commission_asset = models.ForeignKey(AssetBinanceUSDT, on_delete=models.CASCADE, null=False,
                                         related_name='orders_commission')
    datetime = models.DateTimeField(null=False)
    position_side = models.ForeignKey(PositionSideBinanceUSDT, on_delete=models.CASCADE, null=False)
    maker = models.BooleanField()
    buyer = models.BooleanField()
    trade = models.ForeignKey('TradeBinanceUSDT', on_delete=models.CASCADE, null=True, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)


class TradeBinanceUSDT(models.Model):
    is_close = models.BooleanField('Closed trade')
    symbol = models.ForeignKey(SymbolBinanceUSDT, on_delete=models.CASCADE, null=False)
    position_side = models.ForeignKey(PositionSideBinanceUSDT, on_delete=models.CASCADE, null=False)
    open_datetime = models.DateTimeField('Open datetime')
    close_datetime = models.DateTimeField('Close datetime', null=True)
    open_price = models.FloatField('Open price')
    close_price = models.FloatField('Close price', null=True)
    realized_pnl = models.FloatField('Realized Pnl', default=0)
    commission = models.FloatField('Commission', default=0)
    net_profit = models.FloatField('Net Profit', default=0)
    qty = models.FloatField('Qty')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
