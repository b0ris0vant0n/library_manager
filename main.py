from services.book_manager import LibraryManager

def main():
    manager = LibraryManager()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            manager.add_book(title, author, year)
            print("Книга добавлена.")
        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            manager.delete_book(book_id)
            print("Книга удалена.")
        elif choice == "3":
            key = input("Введите параметр для поиска (title, author, year): ")
            value = input("Введите значение: ")
            results = manager.find_books(**{key: value})
            for book in results:
                print(book.to_dict())
        elif choice == "4":
            for book in manager.books:
                print(book.to_dict())
        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            status = input("Введите новый статус (в наличии/выдана): ")
            manager.update_status(book_id, status)
            print("Статус обновлен.")
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()
