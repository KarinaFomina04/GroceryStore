from Utils.localization import Localization


class CommonUtils:
    @staticmethod
    def get_measure(category):
        if category == 3:
            return Localization.get_message('measure_ml')
        else:
            return Localization.get_message('measure_gr')