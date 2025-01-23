from flask import Blueprint, render_template
from .models import Book, User, Loan
from . import db
from datetime import datetime, timedelta
import random
import numpy as np
from collections import Counter
import pandas as pd

# Initialize the Blueprint
main = Blueprint('main', __name__)

### Navigation Routes ###

@main.route('/')
def index():
    """
    Home page.
    """
    return render_template('index.html', title="Home")

@main.route('/books')
def books():
    """
    View all books.
    """
    books = Book.query.all()
    return render_template('books.html', books=books, title="All Books")

@main.route('/books/available')
def available_books():
    """
    View all available books.
    """
    books = Book.query.filter_by(status="available").all()
    return render_template('books.html', books=books, title="Available Books")

@main.route('/books/borrowed')
def borrowed_books():
    """
    View all borrowed books.
    """
    books = Book.query.filter_by(status="borrowed").all()
    return render_template('books.html', books=books, title="Borrowed Books")

@main.route('/users/<int:user_id>/loans')
def user_loans(user_id):
    """
    View loan history for a specific user.
    """
    user = User.query.get_or_404(user_id)
    loans = Loan.query.filter_by(user_id=user_id).all()
    return render_template('user_loans.html', user=user, loans=loans, title=f"{user.name}'s Loans")

@main.route('/statistics')
def statistics():
    """
    Present descriptive statistics about loans.
    """
    # Calculate average loans per user
    avg_loans = Loan.query.count() / User.query.count()

    # Calculate average loan duration (for returned books)
    durations = [
        (pd.to_datetime(loan.return_date) - pd.to_datetime(loan.loan_date)).days
        for loan in Loan.query.filter(Loan.return_date.isnot(None)).all()
    ]
    avg_duration = sum(durations) / len(durations) if durations else 0

    # Get top 10 users by loan count
    user_loan_counts = Counter([loan.user_id for loan in Loan.query.all()])
    top_users = user_loan_counts.most_common(10)

    # Debugging print to verify data
    print("Top Users Data:", top_users)

    return render_template(
        'statistics.html',
        avg_loans=avg_loans,
        avg_duration=avg_duration,
        top_users=top_users,
        title="Statistics"
    )

### Data Simulation Route ###

@main.route('/simulate-data')
def simulate_data():
    """
    Simulate data for Books, Users, and Loans.
    """
    # Clear existing data
    print("Clearing existing data...")
    db.session.query(Loan).delete()
    db.session.query(Book).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Add Books
    print("Adding books...")
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

    # Add Users
    print("Adding users...")
    for i in range(5):
        user = User(name=f"User {i+1}")
        db.session.add(user)

    db.session.commit()

    # Add Loans
    print("Adding loans...")
    users = User.query.all()
    books = Book.query.all()
    for user in users:
        for _ in range(random.randint(3, 10)):
            book = random.choice(books)
            loan_date = datetime.now() - timedelta(days=random.randint(1, 365))
            return_date = None if random.choice([True, False]) else loan_date + timedelta(days=random.randint(1, 30))
            loan = Loan(
                user_id=user.id,
                book_id=book.id,
                loan_date=loan_date.strftime('%Y-%m-%d'),
                return_date=None if not return_date else return_date.strftime('%Y-%m-%d')
            )
            book.status = "borrowed" if not return_date else "available"
            db.session.add(loan)
    db.session.commit()

    print("Data simulation completed!")
    return "Data simulation completed successfully!"
