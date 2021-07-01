from Dao.entity_dao import EntityDAO
from Utils.common_utils import CommonUtils
from Utils.localization import Localization
from Enum.property_enum import ConfirmInputMode


class PropertyDao(EntityDAO):
    def add_property(self, id):
        self.init_connection()
        cursor = self.cursor
        cursor.execute("Select from properties WHERE id =" + id)


