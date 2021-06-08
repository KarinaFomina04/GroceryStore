import psycopg2
import configparser


class CategoryDAO:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        try:
            self.connection = psycopg2.connect(database=config["CONNECTION"]["database"],
                                               user=config["CONNECTION"]["user"],
                                               password=config["CONNECTION"]["password"],
                                               host=config["CONNECTION"]["host"],
                                               port=config["CONNECTION"]["port"]
                                               )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            print("Cannot connect to database")

    def find_all(self):

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
