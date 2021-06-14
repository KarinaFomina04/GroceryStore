from Dao.entity_dao import EntityDAO


class GoodDAO(EntityDAO):

    # TODO this is read (crud)
    def find_by_category_id(self, category_id):
        self.init_connection()

        cursor = self.cursor

        cursor.execute("SELECT * FROM goods WHERE category = " + category_id)

        rows = cursor.fetchall()
        goods = []

        for row in rows:
            good = Good()
            good.set_product_id(row[0])
            good.set_product_name(row[1])
            good.set_category(row[2])
            good.set_weight(row[3])
            good.set_url(row[4])
            good.set_price(row[5])

            goods.append(good)

        print("Operation done successfully")
        self.connection.close()
        return goods

    def find_by_id(self, product_id):
        self.init_connection()

        cursor = self.cursor

        cursor.execute("SELECT * FROM goods WHERE product_id = " + product_id)

        row = cursor.fetchone()

        good = Good()
        good.set_product_id(row[0])
        good.set_product_name(row[1])
        good.set_category(row[2])
        good.set_weight(row[3])
        good.set_url(row[4])
        good.set_price(row[5])

        print("Operation done successfully")
        self.connection.close()
        return good


class Good:

    def get_product_id(self):
        return self.__product_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def get_product_name(self):
        return self.__product_name

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category

    def get_weight(self):
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight

    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price
