from binance_integration.base import BaseOrderSchema


class OrderSchemaUSDT(BaseOrderSchema):
    def __init__(self, order_dict):
        super().__init__(order_dict)

    @property
    def qty(self) -> float:
        self.check_for_detail_data_key('qty')
        return float(self._data['qty'])

    @property
    def quote_qty(self) -> float:
        self.check_for_detail_data_key('quoteQty')
        return float(self._data['quoteQty'])
