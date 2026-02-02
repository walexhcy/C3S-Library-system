from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


class Person(ABC):
    """Abstract class."""

    def __init__(self, person_id: str, name: str) -> None:
        # Encapsulation 
        self._person_id = person_id
        self._name = name

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def role_label(self) -> str:
        """Polymorphism"""
        raise NotImplementedError


class Member(Person):
    """Library member."""

    def role_label(self) -> str:
        return "Member"


class Librarian(Person):
    """Library librarian."""

    def role_label(self) -> str:
        return "Librarian"


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    is_available: bool = True


@dataclass
class Loan:
    loan_id: str
    member_id: str
    book_id: str
