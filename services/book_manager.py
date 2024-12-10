import json
from typing import List

class Book:
    """
    Класс, представляющий книгу в библиотеке.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги ("в наличии" или "выдана").
    """
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Инициализирует объект книги.
        Args:
            book_id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str): Статус книги. По умолчанию "в наличии".
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь.
        Returns:
            dict: Словарь с данными книги.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """
        Создает объект книги из словаря.
        Args:
            data (dict): Словарь с данными книги.
        Returns:
            Book: Объект книги.
        """
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class LibraryManager:
    """
    Класс для управления библиотекой книг.

    Атрибуты:
        storage_file (str): Путь к файлу для хранения данных.
        books (List[Book]): Список книг в библиотеке.
    """
    def __init__(self, storage_file: str = "data/books.json"):
        """
        Инициализирует менеджер библиотеки.

           Args:
           storage_file (str): Путь к файлу для хранения данных. По умолчанию "data/books.json".
        """
        self.storage_file = storage_file
        self.books: List[Book] = self.load_books()

    def load_books(self) -> List[Book]:
        """
        Загружает книги из файла.

            Returns:
            List[Book]: Список объектов книг.
            Raises:
            ValueError: Если данные в файле повреждены или имеют неправильный формат.
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                return [Book.from_dict(book) for book in data]
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, ValueError):
            raise ValueError("Ошибка чтения данных из файла. Убедитесь, что файл JSON имеет правильный формат.")

    def save_books(self):
        """
        Сохраняет список книг в файл.
        """
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.

            Args:
                title (str): Название книги.
                author (str): Автор книги.
                year (int): Год издания книги.
        """
        new_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int):
        """
        Удаляет книгу из библиотеки по ее идентификатору.
               Args:
               book_id (int): Уникальный идентификатор книги.
        """
        self.books = [book for book in self.books if book.id != book_id]
        self.save_books()

    def find_books(self, **kwargs) -> List[Book]:
        """
        Ищет книги по заданным критериям.

            Args:
                **kwargs: Параметры поиска (например, title, author, year).

            Returns:
                List[Book]: Список книг, соответствующих критериям.
        """
        results = self.books
        for key, value in kwargs.items():
            results = [book for book in results if getattr(book, key) == value]
        return results

    def update_status(self, book_id: int, status: str):
        """
            Обновляет статус книги.

            Args:
                book_id (int): Уникальный идентификатор книги.
                status (str): Новый статус книги ("в наличии" или "выдана").
        """
        for book in self.books:
            if book.id == book_id:
                book.status = status
                break
        self.save_books()
