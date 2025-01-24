from app import create_app, db
from app.models import Book, User, Loan
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import argparse
from sqlalchemy.orm import joinedload  # Import for eager loading

# Initialize the Flask app
app = create_app()

def fetch_data():
    """Fetch data from the database with eager loading of the related 'book' for each loan."""
    with app.app_context():
        loans = Loan.query.options(joinedload(Loan.book)).all()  # Eagerly load the 'book' relationship
        books = Book.query.all()
        users = User.query.all()
    return books, loans, users

def calculate_statistics(books, loans, users):
    """Calculate and display descriptive statistics."""
    with app.app_context():  # Ensuring app context for database interaction
        # 1. Author with the most books in the library catalog
        authors = [book.author for book in books]
        author_counts = Counter(authors)
        most_books_author = author_counts.most_common(1)[0]
        print(f"1. Author with the most books: {most_books_author[0]} ({most_books_author[1]} books)")

        # 2. Most borrowed author by all users
        borrowed_authors = [loan.book.author for loan in loans]
        most_borrowed_author = Counter(borrowed_authors).most_common(1)[0]
        print(f"2. Most borrowed author: {most_borrowed_author[0]} ({most_borrowed_author[1]} loans)")

        # 3. Authors exclusively borrowed by each user
        print("\n3. Authors exclusively borrowed by each user:")
        for user in users:
            user_loans = Loan.query.filter_by(user_id=user.id).all()
            user_authors = {loan.book.author for loan in user_loans}
            print(f"   - {user.name}: {', '.join(user_authors) if user_authors else 'No authors borrowed'}")

        # 4. Most borrowed book since the library opened
        borrowed_books = [loan.book.title for loan in loans]
        most_borrowed_book = Counter(borrowed_books).most_common(1)[0]
        print(f"4. Most borrowed book: {most_borrowed_book[0]} ({most_borrowed_book[1]} times)")

        # 5. User with the most simultaneous unreturned loans
        unreturned_loans = Loan.query.filter(Loan.return_date.is_(None)).all()
        user_unreturned_counts = Counter([loan.user_id for loan in unreturned_loans])
        if user_unreturned_counts:
            max_unreturned_user = user_unreturned_counts.most_common(1)[0]
            session = db.session  # Use Session.get() for legacy compatibility
            max_user_name = session.get(User, max_unreturned_user[0]).name
            print(f"5. User with the most unreturned loans: {max_user_name} ({max_unreturned_user[1]} loans)")
        else:
            print("5. No unreturned loans found.")


def plot_probability_density(books):
    """Plot the probability density of Goodreads ratings."""
    ratings = [book.goodread_rating for book in books]
    plt.hist(ratings, bins=10, density=True, alpha=0.7, color='blue')
    plt.title("Goodreads Ratings Probability Density")
    plt.xlabel("Rating")
    plt.ylabel("Density")
    plt.show()

def plot_pages_vs_borrowing_duration(loans):
    """Scatter plot of pages vs borrowing duration."""
    pages = []
    durations = []
    for loan in loans:
        if loan.return_date:
            borrow_time = (pd.to_datetime(loan.return_date) - pd.to_datetime(loan.loan_date)).days
            pages.append(loan.book.pages)  # Accessing loan.book after eager loading
            durations.append(borrow_time)

    plt.scatter(pages, durations, alpha=0.6, c='green')
    plt.title("Pages vs Borrowing Duration")
    plt.xlabel("Pages")
    plt.ylabel("Duration (days)")
    plt.show()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Library Data Analysis")
    parser.add_argument('--statistics', action='store_true', help="Generate statistics")
    parser.add_argument('--plots', action='store_true', help="Generate plots")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    try:
        books, loans, users = fetch_data()

        if args.statistics:
            calculate_statistics(books, loans, users)

        if args.plots:
            plot_probability_density(books)
            plot_pages_vs_borrowing_duration(loans)

    except Exception as e:
        print(f"Error: {e}")
