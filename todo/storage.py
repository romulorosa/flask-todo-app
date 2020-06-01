import abc
import csv
import uuid
import sqlite3


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
            row = [str(item_id), item, status or 'Criado']
            todo_writer.writerow(row)
            return {
                'id': row[0],
                'item': row[1],
                'status': row[2],
            }

    def get_all_items(self) -> list:
        all_items = []
        with open(self._db_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                all_items.append({'id': row[0], 'item': row[1], 'status': row[2]})

        return all_items

    def get_item(self, item_id: str) -> dict:
        with open(self._db_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row_item_id, item, status = row
                if item_id == row_item_id:
                    return {
                        'id': row[0],
                        'item': row[1],
                        'status': row[2],
                    }

    def update_status(self, item_id: str, new_status):
        updated_data = []
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
                updated_data.append({'id': row[0], 'item': row[1], 'status': row[2]})

        return updated_data

    def delete_item(self, item_id):
        updated_data = []
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
                updated_data.append({'id': row[0], 'item': row[1], 'status': row[2]})

        return updated_data


class DatabaseStorage(Storage):
    _db_path = 'todo_database.db'

    def add_item(self, item, status=None):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        status = status or 'Criado'
        sql = 'INSERT INTO todo_items (item, status) VALUES ("%s", "%s");' % (item, status)

        cursor.execute(sql)
        conn.commit()
        conn.close()

        return {'id': cursor.lastrowid, 'item': item, 'status': status}

    def get_all_items(self):
        all_items = []
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        sql = 'SELECT rowid, item, status FROM todo_items;'

        result = cursor.execute(sql).fetchall()
        for row in result:
            all_items.append({'id': row[0], 'item': row[1], 'status': row[2]})

        return all_items

    def get_item(self, item_id):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        sql = 'SELECT rowid, item, status FROM todo_items WHERE rowid=%s;' % (item_id)
        result = cursor.execute(sql).fetchall()
        conn.close()

        item = result[0]

        return {
            'id': item[0],
            'item': item[1],
            'status': item[2],
        }

    def update_status(self, item_id, new_status):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        sql = 'UPDATE todo_items SET status="%s" WHERE rowid=%s;' % (new_status, item_id)
        cursor.execute(sql)
        conn.commit()

        return self.get_item(item_id)

    def delete_item(self, item_id):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        sql = 'DELETE FROM todo_items WHERE rowid=%s;' % item_id
        cursor.execute(sql)
        conn.commit()

        return self.get_all_items()
