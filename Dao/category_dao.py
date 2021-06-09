from Dao.entity_dao import EntityDAO


class CategoryDAO(EntityDAO):

    # TODO this is read (crud)
    def find_all(self):
        self.init_connection()

        cursor = self.cursor

        cursor.execute("SELECT * FROM categories")

        rows = cursor.fetchall()
        categories = []

        for row in rows:
            category = Category()
            category.set_category_id(row[0])
            category.set_category_name(row[1])
            categories.append(category)

        print("Operation done successfully")
        self.connection.close()
        return categories


class Category:

    def get_category_id(self):
        return self.__category_id

    def set_category_id(self, category_id):
        self.__category_id = category_id

    def get_category_name(self):
        return self.__category_name

    def set_category_name(self, category_name):
        self.__category_name = category_name
