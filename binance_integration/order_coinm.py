from binance_integration.base import BaseOrderSchema


class OrderSchemaCOINM(BaseOrderSchema):
    def __init__(self, order_dict):
        super().__init__(order_dict)

    @property
    def pair(self) -> str:
        self.check_for_detail_data_key('pair')
        return self._data['pair']

    @property
    def qty(self) -> float:
        self.check_for_detail_data_key('qty')
        return float(self._data['qty'])

    @property
    def base_qty(self) -> float:
        self.check_for_detail_data_key('baseQty')
        return self._data['baseQty']
