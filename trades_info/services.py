from binance.client import Client
from binance.exceptions import BinanceOrderException, BinanceRequestException, BinanceAPIException

from authorization.models import CustomUser
from trades_info.models import (
    TradeBinanceUSDT,
    SymbolBinanceUSDT,
    AssetBinanceUSDT,
    PositionSideBinanceUSDT,
    OrderBinanceUSDT,
    SideBinanceUSDT,
    TradeBinanceCOINM,
    AssetBinanceCOINM,
    PositionSideBinanceCOINM,
    SideBinanceCOINM,
    SymbolBinanceCOINM,
    PairBinanceCOINM,
    OrderBinanceCOINM,
)
from binance_integration import OrderSchemaUSDT, OrderSchemaCOINM


def _get_binance_client(api_key: str, api_secret: str) -> Client:
    return Client(api_key, api_secret)


def _get_user_balance_usdt(binance_client: Client) -> float:
    balance_list = binance_client.futures_account_balance()

    for balance in balance_list:
        if balance.get('asset') == 'USDT':
            return float(balance['balance'])


def request_to_update_trades_for_users() -> None:
    user_queryset = CustomUser.objects.filter(is_active=True)

    for user in user_queryset:
        try:
            client_for_user_api = _get_binance_client(user.binance_api_key, user.binance_api_secret)

            # updating user acoount balance from binance
            user.balance = _get_user_balance_usdt(client_for_user_api)
            user.save()

            # requests for USDT and COIN-M orders
            orders_usdt = _get_orders_list_usdt(client_for_user_api)
            orders_coinm = _get_orders_list_coinm(client_for_user_api)

            # saving orders to database and combining them to trades
            _save_orders_usdt_to_database(orders_usdt, user)
            _save_orders_coinm_to_database(orders_coinm, user)
        except (BinanceRequestException, BinanceAPIException, BinanceOrderException, AssertionError):
            pass


def _get_orders_list_usdt(binance_client: Client, limit: int = 500) -> list[dict]:
    """Request to Binance API for receive orders from USDT wallet"""
    return binance_client.futures_account_trades(limit=limit, recvWindow=60000)


def _get_orders_list_coinm(binance_client: Client) -> list[list[dict]]:
    """Request to Binance API for receive orders from COINM wallet (for all tickers)"""
    results = []
    symbols = binance_client.futures_coin_symbol_ticker()

    for symbol in symbols:
        result = binance_client.futures_coin_account_trades(symbol=symbol['symbol'], recvWindow=60000)
        if len(result):
            results.append(result)

    return results


def _save_orders_usdt_to_database(order_list: list[dict], user: CustomUser) -> None:
    """Saving orders from USDT wallet to database"""
    for order in order_list:
        _save_order_usdt_to_database(order, user)


def _save_order_usdt_to_database(order_dict: dict, user: CustomUser) -> None:
    """Saving order from USDT wallet to database and combining them to trades"""
    order_schema_usdt = OrderSchemaUSDT(order_dict)
    symbol_instance, created = SymbolBinanceUSDT.objects.get_or_create(name=order_schema_usdt.symbol)
    side_instance, created = SideBinanceUSDT.objects.get_or_create(name=order_schema_usdt.side)
    position_side_instance, created = PositionSideBinanceUSDT.objects.get_or_create(
        name=order_schema_usdt.position_side
    )
    margin_asset_instance, created = AssetBinanceUSDT.objects.get_or_create(name=order_schema_usdt.margin_asset)
    commission_asset_instance, created = AssetBinanceUSDT.objects.get_or_create(name=order_schema_usdt.commission_asset)

    order_usdt_instance, created = OrderBinanceUSDT.objects.get_or_create(
        user=user,
        symbol=symbol_instance,
        side=side_instance,
        position_side=position_side_instance,
        margin_asset=margin_asset_instance,
        commission_asset=commission_asset_instance,
        binance_id=order_schema_usdt.id,
        order_id=order_schema_usdt.order_id,
        price=order_schema_usdt.price,
        qty=order_schema_usdt.qty,
        realized_pnl=order_schema_usdt.realized_pnl,
        quote_qty=order_schema_usdt.quote_qty,
        commission=order_schema_usdt.commission,
        buyer=order_schema_usdt.buyer,
        maker=order_schema_usdt.maker,
        datetime=order_schema_usdt.datetime,
    )

    if created:
        if order_usdt_instance.realized_pnl == float(0):
            try:
                trade_instance = TradeBinanceUSDT.objects.filter(
                    symbol=symbol_instance,
                    open_datetime__lt=order_schema_usdt.datetime,
                    position_side=position_side_instance,
                    is_close=False,
                    user=user,
                ).order_by('open_datetime').reverse()[0]

                trade_instance.realized_pnl += order_usdt_instance.realized_pnl
                trade_instance.qty += order_usdt_instance.qty
                trade_instance.commission += order_usdt_instance.commission
                trade_instance.net_profit = trade_instance.realized_pnl - trade_instance.commission

                order_usdt_instance.trade = trade_instance

                order_usdt_instance.save()
                trade_instance.save()
            except IndexError:
                trade_instance, created = TradeBinanceUSDT.objects.get_or_create(
                    symbol=symbol_instance,
                    open_datetime=order_schema_usdt.datetime,
                    open_price=order_schema_usdt.price,
                    is_close=False,
                    position_side=position_side_instance,
                    realized_pnl=order_schema_usdt.realized_pnl,
                    commission=order_schema_usdt.commission,
                    net_profit=(order_schema_usdt.realized_pnl - order_schema_usdt.commission),
                    qty=order_schema_usdt.qty,
                    user=user,
                )

                if created:
                    order_usdt_instance.trade = trade_instance
                    order_usdt_instance.save()
        else:
            try:
                trade_instance = TradeBinanceUSDT.objects.filter(
                    symbol=symbol_instance,
                    open_datetime__lt=order_schema_usdt.datetime,
                    position_side=position_side_instance,
                    is_close=False,
                    user=user,
                ).order_by('open_datetime').reverse()[0]

                trade_instance.realized_pnl += order_usdt_instance.realized_pnl
                trade_instance.commission += order_usdt_instance.commission
                trade_instance.net_profit = trade_instance.realized_pnl - trade_instance.commission
                trade_instance.qty -= order_usdt_instance.qty
                if trade_instance.qty <= 0:
                    trade_instance.close_datetime = order_usdt_instance.datetime
                    trade_instance.close_price = order_usdt_instance.price
                    trade_instance.is_close = True

                order_usdt_instance.trade = trade_instance

                order_usdt_instance.save()
                trade_instance.save()
            except IndexError:
                pass


def _save_orders_coinm_to_database(order_lists: list[list[dict]], user: CustomUser) -> None:
    """Saving orders from COIN-M wallet to database (for one ticker)"""
    for order_list in order_lists:
        for order in order_list:
            _save_order_coinm_to_database(order, user)


def _save_order_coinm_to_database(order_dict: dict, user: CustomUser) -> None:
    """Saving order from COIN-M wallet to database and combining them to trades"""
    order_schema_coinm = OrderSchemaCOINM(order_dict)
    symbol_instance, created = SymbolBinanceCOINM.objects.get_or_create(name=order_schema_coinm.symbol)
    pair_instance, created = PairBinanceCOINM.objects.get_or_create(name=order_schema_coinm.pair)
    side_instance, created = SideBinanceCOINM.objects.get_or_create(name=order_schema_coinm.side)
    position_side_instance, created = PositionSideBinanceCOINM.objects.get_or_create(
        name=order_schema_coinm.position_side
    )
    margin_asset_instance, created = AssetBinanceCOINM.objects.get_or_create(name=order_schema_coinm.margin_asset)
    commission_asset_instance, created = AssetBinanceCOINM.objects.get_or_create(
        name=order_schema_coinm.commission_asset
    )

    order_coinm_instance, created = OrderBinanceCOINM.objects.get_or_create(
        user=user,
        symbol=symbol_instance,
        pair=pair_instance,
        side=side_instance,
        position_side=position_side_instance,
        margin_asset=margin_asset_instance,
        commission_asset=commission_asset_instance,
        binance_id=order_schema_coinm.id,
        order_id=order_schema_coinm.order_id,
        price=order_schema_coinm.price,
        qty=order_schema_coinm.qty,
        realized_pnl=order_schema_coinm.realized_pnl,
        base_qty=order_schema_coinm.base_qty,
        commission=order_schema_coinm.commission,
        buyer=order_schema_coinm.buyer,
        maker=order_schema_coinm.maker,
        datetime=order_schema_coinm.datetime,
    )

    if created:
        if order_coinm_instance.realized_pnl == float(0):
            try:
                trade_instance = TradeBinanceCOINM.objects.filter(
                    symbol=symbol_instance,
                    open_datetime__lt=order_schema_coinm.datetime,
                    position_side=position_side_instance,
                    is_close=False,
                    user=user,
                ).order_by('open_datetime').reverse()[0]

                trade_instance.realized_pnl += order_coinm_instance.realized_pnl
                trade_instance.commission += order_coinm_instance.commission
                trade_instance.net_profit = trade_instance.realized_pnl - trade_instance.commission
                trade_instance.qty += order_coinm_instance.qty

                order_coinm_instance.trade = trade_instance

                order_coinm_instance.save()
                trade_instance.save()
            except IndexError:
                trade_instance, created = TradeBinanceCOINM.objects.get_or_create(
                    symbol=symbol_instance,
                    open_datetime=order_schema_coinm.datetime,
                    open_price=order_schema_coinm.price,
                    is_close=False,
                    position_side=position_side_instance,
                    realized_pnl=order_schema_coinm.realized_pnl,
                    commission=order_schema_coinm.commission,
                    net_profit=(order_schema_coinm.realized_pnl - order_schema_coinm.commission),
                    qty=order_schema_coinm.qty,
                    user=user,
                )

                if created:
                    order_coinm_instance.trade = trade_instance
                    order_coinm_instance.save()
        else:
            try:
                trade_instance = TradeBinanceCOINM.objects.filter(
                    symbol=symbol_instance,
                    open_datetime__lt=order_schema_coinm.datetime,
                    position_side=position_side_instance,
                    is_close=False,
                    user=user,
                ).order_by('open_datetime').reverse()[0]

                trade_instance.realized_pnl += order_coinm_instance.realized_pnl
                trade_instance.commission += order_coinm_instance.commission
                trade_instance.net_profit = trade_instance.realized_pnl - trade_instance.commission
                trade_instance.qty -= order_coinm_instance.qty
                if trade_instance.qty <= 0:
                    trade_instance.close_datetime = order_coinm_instance.datetime
                    trade_instance.close_price = order_coinm_instance.price
                    trade_instance.is_close = True

                order_coinm_instance.trade = trade_instance

                order_coinm_instance.save()
                trade_instance.save()
            except IndexError:
                pass
