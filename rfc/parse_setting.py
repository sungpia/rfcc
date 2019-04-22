"""
# TODO(chun074@usc.edu): make this singleton object.
This is singleton object.
"""


class ParseSetting:
    __instance = None
    """
    Define an parse setting.
    """
    def __init__(self):
        if ParseSetting.__instance is not None:
            raise Exception("This class is singleton class.")
        else:
            ParseSetting.__instance = self

        # TODO(chun074@usc.edu): loading from external setting makes more sense.
        # might be better pulling from github and set it.
        self._parse_rule = {
            'Redfin Estimate': '//div[@class="info-block avm"]//div[1]',
            'Street Address': '//div[@class="HomeInfo inline-block"]//span[@class="street-address"][1]',
        }

    @staticmethod
    def get_instance(self):
        """ Static access method. """
        if ParseSetting.__instance is None:
            ParseSetting()
        return ParseSetting.__instance

    @staticmethod
    def get_parse_rule(self):
        return self._parse_rule




