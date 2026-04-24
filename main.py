import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox,
    QSpinBox
)

DATA_FILE = 'books.json'
def load_data(file_path=DATA_FILE):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except json.JSONDecodeError:
        # Можно вернуть пустой список или произвести логирование
        return []
    except Exception:
        return []

def save_data(data, file_path=DATA_FILE):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

class BookTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.books = load_data()
        self.filtered_books = self.books.copy()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поля для ввода новой книги
        form_layout = QHBoxLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название книги")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Автор")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Жанр")
        self.pages_input = QSpinBox()
        self.pages_input.setRange(1, 10000)
        self.pages_input.setValue(100)
        self.pages_input.setPrefix("Страницы: ")

        add_button = QPushButton("Добавить книгу")
        add_button.clicked.connect(self.add_book)

        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.author_input)
        form_layout.addWidget(self.genre_input)
        form_layout.addWidget(self.pages_input)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # Таблица для отображения книг
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Автор", "Жанр", "Кол-во страниц"])
        self.load_table()
        layout.addWidget(self.table)

        # Фильтры
        filter_layout = QHBoxLayout()

        self.genre_filter = QLineEdit()
        self.genre_filter.setPlaceholderText("Фильтр по жанру")
        self.genre_filter.textChanged.connect(self.apply_filters)

        self.pages_filter = QComboBox()
        self.pages_filter.addItem("Все")
        self.pages_filter.addItem(">200")
        self.pages_filter.addItem("<=200")
        self.pages_filter.currentIndexChanged.connect(self.apply_filters)

        filter_button = QPushButton("Очистить фильтры")
        filter_button.clicked.connect(self.clear_filters)

        filter_layout.addWidget(QLabel("Фильтр по жанру:"))
        filter_layout.addWidget(self.genre_filter)
        filter_layout.addWidget(QLabel("Страниц:"))
        filter_layout.addWidget(self.pages_filter)
        filter_layout.addWidget(filter_button)

        layout.addLayout(filter_layout)

        self.setLayout(layout)

    def load_table(self):
        self.table.setRowCount(0)
        for book in self.filtered_books:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(book['title']))
            self.table.setItem(row, 1, QTableWidgetItem(book['author']))
            self.table.setItem(row, 2, QTableWidgetItem(book['genre']))
            self.table.setItem(row, 3, QTableWidgetItem(str(book['pages'])))

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        genre = self.genre_input.text().strip()
        pages = self.pages_input.value()

        if not title or not author or not genre:
            QMessageBox.warning(self, "Ошибка", "Поля не должны быть пустыми.")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(new_book)
        self.save_and_refresh()
        self.title_input.clear()
        self.author_input.clear()
        self.genre_input.clear()
        self.pages_input.setValue(100)

    def save_and_refresh(self):
        save_data(self.books)
        self.apply_filters()

    def apply_filters(self):
        genre_filter_text = self.genre_filter.text().lower()
        pages_filter_text = self.pages_filter.currentText()

        self.filtered_books = [
            book for book in self.books
            if (genre_filter_text in book['genre'].lower() or not genre_filter_text)
            and (
                (pages_filter_text == ">200" and book['pages'] > 200) or
                (pages_filter_text == "<=200" and book['pages'] <= 200) or
                (pages_filter_text == "Все")
            )
        ]
        self.load_table()

    def clear_filters(self):
        self.genre_filter.clear()
        self.pages_filter.setCurrentIndex(0)
        self.apply_filters()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookTracker()
    window.show()
    sys.exit(app.exec_())
