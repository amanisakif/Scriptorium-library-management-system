from app import create_app, db
from app.models import Book, User, Loan
from datetime import datetime, timedelta
import random
import numpy as np

app = create_app()

def populate_data():
    """
    Populate the database with sample data for Books, Users, and Loans.
    Includes debugging statements to track progress.
    """
    with app.app_context():
        print("Clearing existing data...")
        db.session.query(Loan).delete()
        db.session.query(Book).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("Database cleared!")  # Debugging print

        # Add Books
        print("Adding books to the database...")
        authors = [f"Author {i+1}" for i in range(10)]
        for i in range(100):
            rating = max(0, min(5, np.random.normal(3.5, 1.0)))
            book = Book(
                title=f"Book {i+1}",
                author=random.choice(authors),
                published_date=f"{random.randint(1900, 2023)}-01-01",
                pages=random.randint(80, 1000),
                goodread_rating=round(rating, 2)
            )
            db.session.add(book)
        print("Books added!")

        # Add Users
        print("Adding users to the database...")
        for i in range(5):
            user = User(name=f"User {i+1}")
            db.session.add(user)
        print("Users added!")

        db.session.commit()
        print("Books and users committed to the database!")

        # Add Loans
        print("Adding loans to the database...")
        users = User.query.all()
        books = Book.query.all()
        for user in users:
            for _ in range(random.randint(3, 10)):  # Each user gets 3-10 loans
                # Select an available book
                available_books = [book for book in books if book.status == "available"]
                if not available_books:
                    break  # No more books available to loan
                book = random.choice(available_books)

                # Generate random loan and return dates
                loan_date = datetime.now() - timedelta(days=random.randint(1, 365))
                return_date = None if random.choice([True, False]) else loan_date + timedelta(days=random.randint(1, 30))

                # Create loan and update book status
                loan = Loan(
                    user_id=user.id,
                    book_id=book.id,
                    loan_date=loan_date.strftime('%Y-%m-%d'),
                    return_date=None if not return_date else return_date.strftime('%Y-%m-%d')
                )
                book.status = "borrowed" if not return_date else "available"
                db.session.add(loan)

        db.session.commit()
        print("Loans added and committed!")
        print("Database populated successfully!")

if __name__ == "__main__":
    populate_data()
