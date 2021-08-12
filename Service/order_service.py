from Dao.order_dao import OrderDAO
from Utils.localization import Localization


class OrderService:
    def __init__(self):
        self.order_dao = OrderDAO()

    def get_orders(self, user_id, is_confirmed):
        orders = self.order_dao.find_orders(user_id)
        text_message = Localization.get_message('your_orders')
        if (orders is not None) and (len(orders) != 0):
            total_price = 0
            for order in orders:
                text_message = text_message + order.get_html_order()
                total_price = total_price + order.get_price() * order.get_count()
            text_message = text_message + Localization.get_message('total_price').format(
                str(total_price))
            if not is_confirmed:
                text_message = text_message + Localization.get_message('properties_added')
            return text_message
        else:
            return Localization.get_message('empty_cart')
