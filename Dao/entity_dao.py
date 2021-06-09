import configparser
import psycopg2


class EntityDAO:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")

    def init_connection(self):
        try:
            self.connection = psycopg2.connect(database=self.config["CONNECTION"]["database"],
                                               user=self.config["CONNECTION"]["user"],
                                               password=self.config["CONNECTION"]["password"],
                                               host=self.config["CONNECTION"]["host"],
                                               port=self.config["CONNECTION"]["port"]
                                               )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            print("Cannot connect to database")
