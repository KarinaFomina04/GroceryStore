from Dao.entity_dao import EntityDAO
from Enum.property_enum import ConfirmInputMode


class PropertyDao(EntityDAO):
    def add_property(self, property_text, property_id, user_id):
        self.init_connection()
        cursor = self.cursor

        cursor.execute("INSERT INTO properties_values (property_value, property_id, user_id) VALUES ( %s,  %s, %s);",
                       (property_text, property_id, user_id))

        print("Operation done successfully")
        self.connection.close()


