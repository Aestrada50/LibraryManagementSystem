from LibraryManagementSystem import LibraryManagementSystem

class Main:

  def main():
    library = LibraryManagementSystem()
    library.run
  if __name__ == "__main__":
    library = LibraryManagementSystem()
    library.load_books_from_csv('Books.csv')
    library.run()