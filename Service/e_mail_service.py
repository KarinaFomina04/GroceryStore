import smtplib
import configparser

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Enum.property_enum import ConfirmInputMode
from Service.order_service import OrderService
from Utils.localization import Localization

msg = MIMEMultipart()

config = configparser.ConfigParser()
config.read("settings.ini")

from_gmail = config["CONNECTION"]["gmail"]
password_gmail = config["CONNECTION"]["password_gmail"]


class EmailService:
    def __init__(self):
        self.order_service = OrderService()

    def send_gmail(self, property_dict, user_id):
        message_text = Localization.get_message('order_in_confirm_email').format(
            property_dict[ConfirmInputMode.NAME.value],
            property_dict[ConfirmInputMode.TELEPHONE_NUMBER.value],
            property_dict[ConfirmInputMode.E_MAIL.value],
            property_dict[ConfirmInputMode.ADDRESS.value]) + self.order_service.get_orders(user_id, True)
        msg['Subject'] = Localization.get_message('сonfirmation_of_order')
        msg.attach(MIMEText(message_text, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_gmail, password_gmail)
        server.sendmail(from_gmail, property_dict[ConfirmInputMode.E_MAIL.value], msg.as_string())
        server.quit()
