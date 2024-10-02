import csv
from Author import Author
from Book import Book
from Customer import Customer

class LibraryManagementSystem:
    def __init__(self):
        self.books = {}  # Dictionary: ISBN -> Book object
        self.authors = {}  # Dictionary: name -> Author object
        self.customers = {}  # Dictionary: customerID -> Customer object
        self.genre_classification = {}  # Dictionary: Genre -> {set of ISBNs}
        self.waitlist = {}  # Dictionary: ISBN -> [list of customerIDs]

    def load_books_from_csv(self, filename):
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Create a Book object from each row
                    book = Book(
                        isbn=int(row['ISBN']),
                        title=row['Title'],
                        author=row['Author Name'],
                        year=int(row['Year']),
                        copies=int(row['Copies']),
                        genre=row['Genre']
                    )

                    # Store the book in the self.books dictionary with ISBN as the key
                    self.books[book.isbn] = book
                    #check if author is in author dictionary already
                    #if not then initialize and add author to authors dictionary and add their book to their set

                    if book.author not in self.authors:
                      author = Author(
                        name = row['Author Name'],
                        birth_year = int(row['Author Birth Year'])
                    )

                      self.authors[author.name] = author
                      self.authors[author.name].add_book(book)

                    #check if genre exists, if not create a key value pair with a set of isbns
                    if book.genre not in self.genre_classification:
                      self.genre_classification[book.genre] = set([book.isbn])

                    #add isbn to set if genre exists
                    self.genre_classification[book.genre].add(book.isbn)


        #except block for case where file does not exist or cannot be found
        except FileNotFoundError:
            print(f"The file {filename} was not found.")
        #except block for other errors that can happen when trying to find file
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_book(self, isbn, title, author_name, author_birth_year, year, copies, genre):
      #initialize the book and add to books dictionary
        newBook = Book(isbn, title, author_name, year, copies, genre)
        self.books[isbn] = newBook

        #check if author is in author dictionary already
        if author_name not in self.authors:
          #if not then initialize author object and add to authors dictionary
          newAuthor = Author(author_name, author_birth_year)
          self.authors[author_name] = newAuthor

        self.authors[author_name].add_book(newBook)

        #check if genre exists, if not create a key value pair with a set of isbns
        if genre not in self.genre_classification:
          self.genre_classification[genre] = set([isbn])

        #add isbn to set if genre exists
        self.genre_classification[genre].add(isbn)

    def register_customer(self, name, email):
      #check if customers dictionary is empty
        if len(self.customers) == 0:
          #if it is then customer's ID is 1
          new_ID = 1

        else:
          #if not then customer's unique ID is 1 greater than latest ID
          new_ID = max(self.customers.keys()) + 1

      #create new customer and add to dictionary
        newCustomer = Customer(new_ID, name, email)
        self.customers[new_ID] = newCustomer

        print(f"Customer has been registered, ID is: {new_ID}")


    def borrow_book(self, isbn, customer_id):
      #check if book is available and customer exists
      if (isbn in self.books) and (customer_id in self.customers):
        #check if the book is available (copies is > 0)
        if self.books[isbn].available_copies > 0:
          #Update the book's available copies.
          self.books[isbn].available_copies -= 1
          #Call the customer's borrow_book method.
          self.customers[customer_id].borrow_book(self.books[isbn])

          #case where the book is unavailable.
        else:
          print('Book is unavailable')
          self.add_to_waitlist(isbn,customer_id)

      #cases where the book or customer doesn't exist
      else:
        if isbn not in self.books:
          print('Book does not exist')
        if customer_id not in self.customers:
          print('Customer does not exist')


    def return_book(self, isbn, customer_id):
      if (isbn in self.books) and (customer_id in self.customers):
          book = self.books[isbn]
          if book in self.customers[customer_id].borrowed_books:
              # Update the book's available copies.
              self.books[isbn].available_copies += 1

              # Handle waitlist
              if self.books[isbn].waitlist:
                  next_customer_id = self.books[isbn].waitlist.popleft(0)  # Get the next person in line
                  self.borrow_book(isbn, next_customer_id)
                  print(f"Book assigned to the next customer on the waitlist (Customer ID: {next_customer_id})")

              # Call the customer's return_book method.
              self.customers[customer_id].return_book(self.books[isbn])



      #Handle cases where the book or customer doesn't exist
      else:
        if isbn not in self.books:
          print('Book does not exist')
        if customer_id not in self.customers:
          print('Customer does not exist')

    def search_books(self, query):
        #Allow searching by title, author name, or ISBN.
        #query = input('search by title, author name, or ISBN? \n')
        results = []
        queryStr = str(query).lower()

        #if the input is a digit it means they must be searching by ISBN
        if query.isnumeric() and len(query) in [10, 13]:
          for isbn in self.books:
            if query == isbn:
              results.append(self.books[isbn])

        else:
          for value in self.books.values():
           if (queryStr == value.title.lower()) or (queryStr == value.author.lower()):
            results.append(value)

        # print a list of matching Book objects.
        for book in results:
          print(book)

    def display_available_books(self):
        #iterate through the book values in the books dictionary
        for book in self.books.values():
          #if the book is available then append to the avlBooks list
          if book.available_copies > 0:
            print(book)

    def display_customer_books(self, customer_id):
        if customer_id in self.customers:
          #return a list of the keys in borrowed_books as those are the books the customer has borrowed
          for book in self.customers[customer_id].borrowed_books.keys():
            print(book)


    def recommend_books(self, customer_id):
        #initialize a set of genres to make sure there are no duplicartes
        genres = set()
        rec = []

        #iterate through customer's borrowed books
        for book in self.customers[customer_id].borrowed_books.keys():
          genres.add(book.genre)

        #iterate through all books in library
        for book in self.books.values():
          # check if genre matches customer's genre list, that the reccomendation list does not exceed 5
          # also check that the customer has not already checked out the book

          if book.genre in genres and len(rec)<5 and book not in self.customers[customer_id].borrowed_books:
            rec.append(book)
        for book in rec:
          print(book)


    def add_to_waitlist(self, isbn, customer_id):
        self.books[isbn].waitlist.append(customer_id)


    def check_late_returns(self, days_threshold=14):
        late = []
        for customer in self.customers.values():
          for book, date in customer.borrowed_books.items():
            if date > days_threshold:
              late.append(book)




    def run(self):

        go = True
        while(go == True):
          choice = int(input("""
          1. Add Book
          2. Register Customer
          3. Borrow Book
          4. Return Book
          5. Search Books
          6. Display Available Books
          7. Display Customers Borrowed Books
          8. Recommend Books
          9. Check Late Returns
          10. Exit
          """))

          if choice < 1 or choice > 10:

            print('Invalid option, please enter a valid option')



          if choice == 1:
            isbn = int(input('\nInput ibsn number : '))
            title = input( 'Input title of book:  ')
            author_name = input('Input the author of the book:  ')
            author_birth_year = input("Input the author's birth year: ")
            year = input('Input the year of the book: ')
            copies = int(input( 'Input the number of copies for this title:  '))
            genre = input('Input the genre of book: ')

            self.add_book(isbn, title, author_name, author_birth_year, year, copies, genre)





          if choice == 2:
            name = input('\nInput customer name: ')
            email = input('Input new customer email: ')
            self.register_customer(name,email)



          if choice == 3:
            customer_id = int(input('\nPlease enter your cutomer ID: '))
            isbn = int(input('Please enter the ISBN of the book you would like to borrow: '))
            self.borrow_book(isbn,customer_id)



          if choice == 4:
            customer_id = int(input('Please enter your cutomer ID to proceed: '))
            isbn = int(input('Please enter the ISBN of the book you would like to return: '))
            self.return_book(isbn,customer_id)



          if choice == 5:
            book_info = input("\nEnter Title, Author Name, or ISBN for the book you're searching for: ")
            self.search_books(book_info)



          if choice == 6:
              print('Displaying Available books: ')
              self.display_available_books()


          if choice == 7:
            customer_id = int(input("\nPlease enter customer id: "))
            print("Displaying Customer's Borrowed books: ")
            self.display_customer_books(customer_id)



          if choice == 8:
            customer_id = int(input("\nPlease enter customer id: "))
            print('Displaying Recommended books: ')
            self.recommend_books(customer_id)


          if choice ==9:
              print('\nList of late returns: ')
              self.check_late_returns(days_threshold=14)

          if choice == 10:
            print("goodbye!")
            go = False