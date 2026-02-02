from __future__ import annotations
from typing import List, Optional
import uuid

from app.models import Book, Member, Loan
from app.storage import JsonStorage


class LibrarySystem:
    """Business logic"""

    def __init__(self, storage: JsonStorage) -> None:
        self._storage = storage
        self._data = self._storage.load()

        self._books: List[Book] = [Book(**b) for b in self._data.get("books", [])]
        self._members: List[Member] = [
            Member(m["person_id"], m["name"]) for m in self._data.get("members", [])
        ]
        self._loans: List[Loan] = [Loan(**l) for l in self._data.get("loans", [])]

    # Persistence
    def _sync_and_save(self) -> None:
        self._data["books"] = [b.__dict__ for b in self._books]
        self._data["members"] = [{"person_id": m.person_id, "name": m.name} for m in self._members]
        self._data["loans"] = [l.__dict__ for l in self._loans]
        self._storage.save(self._data)

    # Books
    def list_books(self) -> List[Book]:
        return list(self._books)

    def add_book(self, title: str, author: str) -> Book:
        book = Book(
            book_id=str(uuid.uuid4())[:8],
            title=title.strip(),
            author=author.strip(),
            is_available=True
        )
        self._books.append(book)
        self._sync_and_save()
        return book

    def find_book(self, book_id: str) -> Optional[Book]:
        for b in self._books:
            if b.book_id == book_id:
                return b
        return None

    def remove_book(self, book_id: str) -> None:
        book = self.find_book(book_id)
        if not book:
            raise ValueError("Book not found.")
        if not book.is_available:
            raise ValueError("Cannot remove a borrowed book.")
        self._books = [b for b in self._books if b.book_id != book_id]
        self._sync_and_save()

    # Members
    def list_members(self) -> List[Member]:
        return list(self._members)

    def add_member(self, member_id: str, name: str) -> Member:
        member_id = member_id.strip()
        if any(m.person_id == member_id for m in self._members):
            raise ValueError("Member ID already exists.")
        m = Member(member_id, name.strip())
        self._members.append(m)
        self._sync_and_save()
        return m

    def find_member(self, member_id: str) -> Optional[Member]:
        for m in self._members:
            if m.person_id == member_id:
                return m
        return None

    def remove_member(self, member_id: str) -> None:
        member = self.find_member(member_id)
        if not member:
            raise ValueError("Member not found.")
        if any(l.member_id == member_id for l in self._loans):
            raise ValueError("Cannot remove member with active loans.")
        self._members = [m for m in self._members if m.person_id != member_id]
        self._sync_and_save()

    # Loans
    def list_loans(self) -> List[Loan]:
        return list(self._loans)

    def borrow_book(self, member_id: str, book_id: str) -> Loan:
        member = self.find_member(member_id)
        if not member:
            raise ValueError("Member not found.")

        book = self.find_book(book_id)
        if not book:
            raise ValueError("Book not found.")
        if not book.is_available:
            raise ValueError("Book is already borrowed.")

        loan = Loan(
            loan_id=str(uuid.uuid4())[:8],
            member_id=member_id,
            book_id=book_id
        )
        self._loans.append(loan)
        book.is_available = False
        self._sync_and_save()
        return loan

    def return_book(self, loan_id: str) -> None:
        loan = next((l for l in self._loans if l.loan_id == loan_id), None)
        if not loan:
            raise ValueError("Loan not found.")

        book = self.find_book(loan.book_id)
        if book:
            book.is_available = True

        self._loans = [l for l in self._loans if l.loan_id != loan_id]
        self._sync_and_save()
