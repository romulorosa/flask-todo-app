import abc
import csv
import uuid


class Storage(metaclass=abc.ABCMeta):
    def add_item(self, item, status):
        pass

    def get_all_items(self):
        pass

    def get_item(self, item_id):
        pass

    def update_status(self, item_id, new_status):
        pass

    def delete_item(self, item_id):
        pass


class FileStorage(Storage):
    _db_path = 'todo_database.csv'

    def add_item(self, item: str, status: str = None):
        with open(self._db_path, mode='a') as csv_file:
            todo_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )
            item_id = uuid.uuid4()
            item_row = [str(item_id), item, status or 'Criado']
            todo_writer.writerow(item_row)
            return item_row

    def get_all_items(self) -> list:
        with open(self._db_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            return [row for row in csv_reader]

    def get_item(self, item_id: str) -> list:
        with open(self._db_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row_item_id, item, status = row
                if item_id == row_item_id:
                    return row

    def update_status(self, item_id: str, new_status) :
        with open(self._db_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            new_data = []
            for row in csv_reader:
                row_item_id, item, status = row
                if item_id == row_item_id:
                    row = [row_item_id, item, new_status]
                new_data.append(row)

        with open(self._db_path, mode='w') as csv_file:
            todo_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )
            for row in new_data:
                todo_writer.writerow(row)
        return new_data

    def delete_item(self, item_id):
        with open(self._db_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            new_data = []
            for row in csv_reader:
                row_item_id, item, status = row
                if not item_id == row_item_id:
                    new_data.append(row)

        with open(self._db_path, mode='w') as csv_file:
            todo_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )
            for row in new_data:
                todo_writer.writerow(row)
        return new_data

