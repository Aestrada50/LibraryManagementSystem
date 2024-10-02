class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.borrowed_books = {}

    def borrow_book(self, book):
        if book in self.borrowed_books:
          print('Book is already checked out!')
        else:
          self.borrowed_books[book] = 0
          print('book checked out successfully')


    def return_book(self, book):
        if book in self.borrowed_books:
          self.borrowed_books.pop(book)
          print('Book returned successfully')
        else:
          print('Book is not checked out')

    def get_borrowed_books(self):
        return self.borrowed_books.keys()