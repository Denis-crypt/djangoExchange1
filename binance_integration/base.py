from datetime import datetime


class BaseOrderSchema:
    def __init__(self, order_dict: dict):
        self._data = order_dict

    def check_for_detail_data_key(self, key) -> None:
        """Some keys are only in the detail response, raise an
        exception if the key is not found."""

        if key not in self._data:
            raise AttributeError(
                f"{key} is not in data, please make sure this is a detail response."
            )

    @property
    def datetime(self) -> datetime:
        self.check_for_detail_data_key('time')
        return datetime.fromtimestamp(self._data['time']/1000)

    @property
    def symbol(self) -> str:
        self.check_for_detail_data_key('symbol')
        return self._data['symbol']

    @property
    def id(self) -> int:
        self.check_for_detail_data_key('id')
        return self._data['id']

    @property
    def order_id(self) -> int:
        self.check_for_detail_data_key('orderId')
        return self._data['orderId']

    @property
    def side(self) -> str:
        self.check_for_detail_data_key('side')
        return self._data['side']

    @property
    def price(self) -> float:
        self.check_for_detail_data_key('price')
        return float(self._data['price'])

    @property
    def realized_pnl(self) -> float:
        self.check_for_detail_data_key('realizedPnl')
        return float(self._data['realizedPnl'])

    @property
    def margin_asset(self) -> str:
        self.check_for_detail_data_key('marginAsset')
        return self._data['marginAsset']

    @property
    def commission(self) -> float:
        self.check_for_detail_data_key('commission')
        return float(self._data['commission'])

    @property
    def commission_asset(self) -> str:
        self.check_for_detail_data_key('commissionAsset')
        return self._data['commissionAsset']

    @property
    def position_side(self) -> str:
        self.check_for_detail_data_key('positionSide')
        return self._data['positionSide']

    @property
    def maker(self) -> bool:
        self.check_for_detail_data_key('maker')
        return self._data['maker']

    @property
    def buyer(self) -> bool:
        self.check_for_detail_data_key('buyer')
        return self._data['buyer']
