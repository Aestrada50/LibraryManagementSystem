# Library Management System

## Overview

This **Library Management System** is a simple console-based application designed to manage a library's core operations such as managing books, customers, and authors. It allows users to view, add, update, and delete books and customers in the library system.

## Features

- **Book Management:**
  - Add, update, and delete books.
  - view entire selection
  - View book details, including title, author, and availability.
  - get personalized reccomendations

- **Customer Management:**
  - Add, update, and delete customer information.
  - Track which books customers have borrowed or returned.

- **Author Management:**
  - Manage details about authors related to the books in the library.

## Project Structure

The project contains the following main files:

- **Author.py**: Handles operations related to author data.
- **Book.py**: Contains classes and functions for book management, such as adding and removing books.
- **Books.csv**: A CSV file storing information about books in the library.
- **Customer.py**: Manages customer-related data and functionality.
- **LibraryManagementSystem.py**: The main library system file that integrates book, author, and customer management functions.
- **Main.py**: The entry point for the system, coordinating user input and displaying options to interact with the system.
- **\_\_pycache\_\_/**: Directory with cached bytecode versions of Python files.

## Requirements

- Python 3.8 or higher
- Libraries/Modules:
  - CSV module (to manage CSV file handling)
  
> *All necessary Python libraries are built-in and require no additional installation.*

## Installation

1. Clone the repository to your local machine:

git clone https://github.com/Aestrada50/LibraryManagementSystem.git

Navigate to the project directory:

cd LibraryManagementSystem

Usage
Run the Main.py file to start the application:

python Main.py

The system will prompt you with various options to manage books, authors, and customers. You can select from the below options:

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
