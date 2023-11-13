import pickle

# The class definition must be available in the namespace when unpickling
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        
    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"

# Unpickle the book instance
with open('book.pkl', 'rb') as file:
    loaded_book = pickle.load(file)

print(loaded_book)
