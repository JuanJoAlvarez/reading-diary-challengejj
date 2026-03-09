from datetime import datetime


class Note:
    def __init__(self, text: str, page: int, date: datetime):
        self.text = text
        self.page = page
        self.date = date

    def __str__(self) -> str:
        return f"{self.date} - page {self.page}: {self.text}"


class Book:
    EXCELLENT = 3
    GOOD = 2
    BAD = 1
    UNRATED = -1

    def __init__(self, isbn: str, title: str, author: str, pages: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.pages = pages
        self.rating = Book.UNRATED
        self.notes: list[Note] = []

    def add_note(self, text: str, page: int, date: datetime) -> bool:
        if page > self.pages:
            return False
        note = Note(text, page, date)
        self.notes.append(note)
        return True

    def set_rating(self, rating: int) -> bool:
        if rating not in (Book.EXCELLENT, Book.GOOD, Book.BAD):
            return False
        self.rating = rating
        return True

    def get_notes_of_page(self, page: int) -> list[Note]:
        return [note for note in self.notes if note.page == page]

    def page_with_most_notes(self) -> int:
        if not self.notes:
            return -1

        count = {}
        for note in self.notes:
            count[note.page] = count.get(note.page, 0) + 1

        return max(count, key=count.get)

    def __str__(self) -> str:
        rating_map = {
            Book.EXCELLENT: "excellent",
            Book.GOOD: "good",
            Book.BAD: "bad",
            Book.UNRATED: "unrated"
        }

        rating_str = rating_map[self.rating]

        return (
            f"ISBN: {self.isbn}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Pages: {self.pages}\n"
            f"Rating: {rating_str}"
        )


class ReadingDiary:
    def __init__(self):
        self.books: dict[str, Book] = {}

    def add_book(self, isbn: str, title: str, author: str, pages: int) -> bool:
        if isbn in self.books:
            return False

        book = Book(isbn, title, author, pages)
        self.books[isbn] = book
        return True

    def search_by_isbn(self, isbn: str) -> Book | None:
        return self.books.get(isbn)

    def add_note_to_book(self, isbn: str, text: str, page: int, date: datetime) -> bool:
        book = self.search_by_isbn(isbn)
        if book is None:
            return False
        return book.add_note(text, page, date)

    def rate_book(self, isbn: str, rating: int) -> bool:
        book = self.search_by_isbn(isbn)
        if book is None:
            return False
        return book.set_rating(rating)

    def book_with_most_notes(self) -> Book | None:
        if not self.books:
            return None

        max_notes = 0
        result = None

        for book in self.books.values():
            if len(book.notes) > max_notes:
                max_notes = len(book.notes)
                result = book

        if max_notes == 0:
            return None

        return result