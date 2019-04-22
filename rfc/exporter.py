import csv


class Exporter:
    """
    class Expoter are used to export data into different formats.
    """

    @staticmethod
    def to_my_sql(self, data):
        # basically, connect to DB,
        # then use flattened dict (key, value) to (column, value)
        # if not supported by DBMS, transaction should be atomic, use related library or function provided.
        pass

    @staticmethod
    def to_csv(file_name, dataset):
        f = open(file_name, 'w')
        w = csv.DictWriter(f, dataset[0].keys())
        w.writeheader()
        w.writerows(dataset)
        f.close()
