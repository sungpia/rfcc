class Formatter:
    @staticmethod
    def trim(raw):
        return raw.strip().replace('$', '').replace(',', '')

    @staticmethod
    def format(self, data):
        for category in data:
            for label in data[category]:
                raws = data[category][label]
                formatted = list()
                for raw in raws:
                    trimmed = self.trim(raw)
                    if trimmed != '':
                        formatted.append(trimmed)
                data[category][label] = formatted
        return data

    @staticmethod
    def flatten(data):
        flat_dict = dict()
        for category in data:
            for label in data[category]:
                if len(data[category][label]) == 1:
                    flat_dict[category + "|" + label] = data[category][label][0]
                else:
                    flat_dict[category + "|" + label] = str(data[category][label])
        return flat_dict
