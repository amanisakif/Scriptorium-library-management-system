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
    View all books with total count.
    """
    books = Book.query.all()
    total_books = len(books)
    return render_template('books.html', books=books, title="All Books", total=total_books)

@main.route('/books/available')
def available_books():
    """
    View all available books with total count.
    """
    books = Book.query.filter_by(status="available").all()
    total_available = len(books)
    return render_template('books.html', books=books, title="Available Books", total=total_available)

@main.route('/books/borrowed')
def borrowed_books():
    """
    View all borrowed books with total count.
    """
    books = Book.query.filter_by(status="borrowed").all()
    total_borrowed = len(books)
    return render_template('books.html', books=books, title="Borrowed Books", total=total_borrowed)

@main.route('/users/<int:user_id>/loans')
def user_loans(user_id):
    """
    View loan history for a specific user.
    """
    user = User.query.get_or_404(user_id)
    current_loans = Loan.query.filter_by(user_id=user_id, return_date=None).all()
    past_loans = Loan.query.filter_by(user_id=user_id).filter(Loan.return_date.isnot(None)).all()
    return render_template('user_loans.html', user=user, current_loans=current_loans, past_loans=past_loans, title=f"{user.name}'s Loan History")

@main.route('/users')
def all_users():
    """
    View all users' loan histories.
    """
    users = User.query.all()
    return render_template('all_users.html', users=users, title="All Users")

@main.route('/statistics')
def statistics():
    """
    Generate and display library statistics.
    """
    try:
        # Calculate average loans per user
        user_count = User.query.count()
        avg_loans = Loan.query.count() / user_count if user_count > 0 else 0

        # Calculate average loan duration (for returned books)
        durations = [
            (pd.to_datetime(loan.return_date) - pd.to_datetime(loan.loan_date)).days
            for loan in Loan.query.filter(Loan.return_date.isnot(None)).all()
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # Calculate borrowing trends (loans over time)
        loan_dates = [pd.to_datetime(loan.loan_date) for loan in Loan.query.all()]
        loan_df = pd.DataFrame({'Date': loan_dates})
        loan_df['Month'] = loan_df['Date'].dt.to_period('M')
        borrowing_trends = loan_df['Month'].value_counts().sort_index()
        borrowing_trends_labels = borrowing_trends.index.astype(str).tolist()
        borrowing_trends_data = borrowing_trends.values.tolist()

        # Top 3 users with the most loans
        top_users = db.session.query(
            User.name, db.func.count(Loan.id).label('loan_count')
        ).join(Loan).group_by(User.name).order_by(db.desc('loan_count')).limit(3).all()

        return render_template(
            'statistics.html',
            avg_loans=round(avg_loans, 2),
            avg_duration=round(avg_duration, 2),
            borrowing_trends_labels=borrowing_trends_labels,
            borrowing_trends_data=borrowing_trends_data,
            top_users=top_users
        )
    except Exception as e:
        print(f"Error in /statistics route: {e}")
        return "An error occurred while generating statistics.", 500

### Data Simulation Route ###

@main.route('/simulate-data')
def simulate_data():
    """
    Simulate data for Books, Users, and Loans.
    """
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(Loan).delete()
        db.session.query(Book).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("Existing data cleared.")

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
        print("Books added.")

        # Add Users
        print("Adding users...")
        for i in range(5):
            user = User(name=f"User {i+1}")
            db.session.add(user)
        print("Users added.")

        db.session.commit()

        # Add Loans
        print("Adding loans...")
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
        print("Loans added.")

        print("Data simulation completed!")
        return "Data simulation completed successfully!"
    except Exception as e:
        print(f"Error in /simulate-data route: {e}")
        return "An error occurred during data simulation.", 500
