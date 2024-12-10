import unittest
import os
import json
from services.book_manager import LibraryManager, Book


class TestLibraryManager(unittest.TestCase):
    TEMP_FILE = "temp_books.json"

    def setUp(self):
        """Создает временный файл перед каждым тестом."""
        with open(self.TEMP_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)
        self.manager = LibraryManager(storage_file=self.TEMP_FILE)

    def tearDown(self):
        """Удаляет временный файл после каждого теста."""
        if os.path.exists(self.TEMP_FILE):
            os.remove(self.TEMP_FILE)

    def test_add_book(self):
        """Тест добавления книги."""
        self.manager.add_book("Гарри Поттер", "Дж. К. Роулинг", 1997)
        self.assertEqual(len(self.manager.books), 1)
        self.assertEqual(self.manager.books[0].title, "Гарри Поттер")

    def test_delete_book(self):
        """Тест удаления книги."""
        self.manager.add_book("Гарри Поттер", "Дж. К. Роулинг", 1997)
        book_id = self.manager.books[0].id
        self.manager.delete_book(book_id)
        self.assertEqual(len(self.manager.books), 0)

    def test_find_book_by_title(self):
        """Тест поиска книги по названию."""
        self.manager.add_book("Гарри Поттер", "Дж. К. Роулинг", 1997)
        results = self.manager.find_books(title="Гарри Поттер")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Дж. К. Роулинг")

    def test_update_status(self):
        """Тест изменения статуса книги."""
        self.manager.add_book("Гарри Поттер", "Дж. К. Роулинг", 1997)
        book_id = self.manager.books[0].id
        self.manager.update_status(book_id, "выдана")
        self.assertEqual(self.manager.books[0].status, "выдана")

    def test_load_empty_books(self):
        """Тест загрузки пустого списка книг."""
        self.assertEqual(len(self.manager.books), 0)

    def test_save_and_load_books(self):
        """Тест сохранения и загрузки книг."""
        self.manager.add_book("Гарри Поттер", "Дж. К. Роулинг", 1997)
        new_manager = LibraryManager(storage_file=self.TEMP_FILE)
        self.assertEqual(len(new_manager.books), 1)
        self.assertEqual(new_manager.books[0].title, "Гарри Поттер")
