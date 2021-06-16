from Dao.entity_dao import EntityDAO


class OrderDAO(EntityDAO):
    def add_to_cart(self, user_id, product_id):
        self.init_connection()

        cursor = self.cursor

        cursor.execute(
            "SELECT * FROM public.order WHERE user_id = " + str(user_id) + " AND product_id = " + str(product_id))
        is_good_exist = cursor.fetchone() is not None

        if is_good_exist:
            cursor.execute("UPDATE public.order SET count = count + 1 WHERE user_id = " + str(user_id) +
                           " AND product_id = " + str(product_id))
        else:
            cursor.execute("INSERT INTO public.order (user_id, product_id) VALUES ( %s,  %s);", (user_id, product_id))

        print("Operation done successfully")
        self.connection.close()

    def find_orders(self, user_id):
        self.init_connection()

        cursor = self.cursor

        cursor.execute("SELECT public.order.order_id, goods.product_name, goods.weight, goods.price, goods.category,"
                       " public.order.count"
                       " FROM public.order JOIN goods ON goods.product_id = public.order.product_id WHERE"
                       " public.order.user_id =" + str(user_id))

        rows = cursor.fetchall()
        orders = []

        for row in rows:
            order = Order()
            order.set_order_id(row[0])
            order.set_product_name(row[1])
            order.set_weight(row[2])
            order.set_price(row[3])
            order.set_category(row[4])
            order.set_count(row[5])

            orders.append(order)

        print("Operation done successfully")
        self.connection.close()
        return orders


class Order:
    def get_order_id(self):
        return self.__order_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def get_product_name(self):
        return self.__product_name

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def get_weight(self):
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category

    def get_count(self):
        return self.__count

    def set_count(self, count):
        self.__count = count
