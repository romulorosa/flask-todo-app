import unittest
import os
from storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.storage._db_path = 'todo_test_database.csv'

    def tearDown(self) -> None:
        os.remove(self.storage._db_path)


class TestTodoFileStorageAddItem(TestFileStorage):
    def test_add_item(self,):
        response = self.storage.add_item('Test', 'New')
        item_name = 'Test'
        item_status = 'New'

        self.assertEqual(response['item'], item_name)
        self.assertEqual(response['status'], item_status)


class TestTodoFileStorageGetItem(TestFileStorage):
    def setUp(self):
        super(TestTodoFileStorageGetItem, self).setUp()
        self.item = self.storage.add_item('My Task')

    def test_get_item(self):
        response = self.storage.get_item(self.item['id'])
        self.assertEqual(response['id'], self.item['id'])
        self.assertEqual(response['item'], self.item['item'])
        self.assertEqual(response['status'], self.item['status'])


if __name__ == '__main__':
    unittest.main()
