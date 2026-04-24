import unittest
import os
import json
from main import load_data, save_data

class TestDataFunctions(unittest.TestCase):
    TEST_FILE = 'test_books.json'

    def tearDown(self):
        # Очистка файла после тестов
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_save_and_load_data(self):
        test_data = [
            {"title": "Test Book 1", "author": "Author 1", "genre": "Genre 1", "pages": 123},
            {"title": "Test Book 2", "author": "Author 2", "genre": "Genre 2", "pages": 456},
        ]

        # Проверка сохранения
        save_data(test_data, self.TEST_FILE)
        self.assertTrue(os.path.exists(self.TEST_FILE))

        # Проверка загрузки
        loaded_data = load_data(self.TEST_FILE)
        self.assertEqual(loaded_data, test_data)

    def test_load_data_empty(self):
        # Проверка работы с несуществующим файлом
        data = load_data('non_existent.json')
        self.assertEqual(data, [])

    def test_load_data_malformed(self):
        # Создаём повреждённый файл
        with open(self.TEST_FILE, 'w', encoding='utf-8') as f:
            f.write('{"invalid_json": }')
        # Конвертация должна возвращать пустой список
        result = load_data(self.TEST_FILE)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
