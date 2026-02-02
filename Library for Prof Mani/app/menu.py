from app.storage import JsonStorage
from app.library import LibrarySystem


class MenuApp:
    """Console UI"""

    def __init__(self) -> None:
        self._storage = JsonStorage("data/library.json")
        self._lib = LibrarySystem(self._storage)

    def run(self) -> None:
        while True:
            print("\n=== MAIN MENU ===")
            print("1) Books")
            print("2) Members")
            print("3) Loans")
            print("0) Exit")
            choice = input("Select: ").strip()

            if choice == "1":
                self._books_menu()
            elif choice == "2":
                self._members_menu()
            elif choice == "3":
                self._loans_menu()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

    # Sub-menus
    def _books_menu(self) -> None:
        while True:
            print("\nBOOKS MENU")
            print("1) List books")
            print("2) Add book")
            print("3) Remove book")
            print("0) Back")
            c = input("Select: ").strip()

            if c == "1":
                books = self._lib.list_books()
                if not books:
                    print("No books found.")
                for b in books:
                    status = "Available" if b.is_available else "Borrowed"
                    print(f"- [{b.book_id}] {b.title} by {b.author} ({status})")
            elif c == "2":
                title = input("Title: ")
                author = input("Author: ")
                book = self._lib.add_book(title, author)
                print(f"Added book with id: {book.book_id}")
            elif c == "3":
                book_id = input("Book ID to remove: ").strip()
                try:
                    self._lib.remove_book(book_id)
                    print("Book removed.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif c == "0":
                return
            else:
                print("Invalid option.")

    def _members_menu(self) -> None:
        while True:
            print("\nMEMBERS MENU")
            print("1) List members")
            print("2) Add member")
            print("3) Remove member")
            print("0) Back")
            c = input("Select: ").strip()

            if c == "1":
                members = self._lib.list_members()
                if not members:
                    print("No members found.")
                for m in members:
                    print(f"- [{m.person_id}] {m.name} ({m.role_label()})")
            elif c == "2":
                member_id = input("Member ID: ")
                name = input("Name: ")
                try:
                    m = self._lib.add_member(member_id, name)
                    print(f"Added member: {m.person_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            elif c == "3":
                member_id = input("Member ID to remove: ").strip()
                try:
                    self._lib.remove_member(member_id)
                    print("Member removed.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif c == "0":
                return
            else:
                print("Invalid option.")

    def _loans_menu(self) -> None:
        while True:
            print("\nLOANS MENU")
            print("1) List loans")
            print("2) Borrow book")
            print("3) Return book")
            print("0) Back")
            c = input("Select: ").strip()

            if c == "1":
                loans = self._lib.list_loans()
                if not loans:
                    print("No loans found.")
                for l in loans:
                    print(f"- Loan[{l.loan_id}] Member={l.member_id} Book={l.book_id}")
            elif c == "2":
                member_id = input("Member ID: ")
                book_id = input("Book ID: ")
                try:
                    loan = self._lib.borrow_book(member_id, book_id)
                    print(f"Borrowed! Loan id: {loan.loan_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            elif c == "3":
                loan_id = input("Loan ID: ")
                try:
                    self._lib.return_book(loan_id)
                    print("Returned successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif c == "0":
                return
            else:
                print("Invalid option.")
