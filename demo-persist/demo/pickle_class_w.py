import pickle

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        
    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"

# Create an instance of the Book class
book_instance = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="1234567890")

# Pickle the book instance
with open('book.pkl', 'wb') as file:
    pickle.dump(book_instance, file)
