from app import create_app
from app.models import Book, User, Loan
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Initialize the Flask app
app = create_app()

def fetch_data():
    """Fetch data from the database."""
    loans = Loan.query.all()
    books = Book.query.all()
    users = User.query.all()
    return books, loans, users

def calculate_statistics(books, loans, users):
    """Calculate and display descriptive statistics."""
    # 1. Author with the most books in the library catalog
    authors = [book.author for book in books]
    author_counts = Counter(authors)
    most_books_author = author_counts.most_common(1)[0]
    print(f"\n1. Author with the most books: {most_books_author[0]} ({most_books_author[1]} books)")

    # 2. Most borrowed author by all users
    borrowed_authors = [loan.book.author for loan in loans]
    most_borrowed_author = Counter(borrowed_authors).most_common(1)[0]
    print(f"2. Most borrowed author: {most_borrowed_author[0]} ({most_borrowed_author[1]} loans)")

    # 3. List of authors exclusively borrowed by each user
    print("\n3. Authors exclusively borrowed by each user:")
    for user in users:
        user_loans = Loan.query.filter_by(user_id=user.id).all()
        user_authors = {loan.book.author for loan in user_loans}
        print(f"   - {user.name}: {', '.join(user_authors) if user_authors else 'No authors borrowed'}")

    # 4. Most borrowed book since the library opened
    borrowed_books = [loan.book.title for loan in loans]
    most_borrowed_book = Counter(borrowed_books).most_common(1)[0]
    print(f"\n4. Most borrowed book: {most_borrowed_book[0]} ({most_borrowed_book[1]} times)")

    # 5. User with the most simultaneous unreturned loans
    unreturned_loans = Loan.query.filter(Loan.return_date.is_(None)).all()
    user_unreturned_counts = Counter([loan.user_id for loan in unreturned_loans])
    if user_unreturned_counts:
        max_unreturned_user = user_unreturned_counts.most_common(1)[0]
        max_user_name = User.query.get(max_unreturned_user[0]).name
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
            pages.append(loan.book.pages)
            durations.append(borrow_time)

    plt.scatter(pages, durations, alpha=0.6, c='green')
    plt.title("Pages vs Borrowing Duration")
    plt.xlabel("Pages")
    plt.ylabel("Duration (days)")
    plt.show()

def plot_top_borrowed_authors(author_counts):
    """Bar chart of the top 3 most borrowed authors."""
    top_authors = author_counts.most_common(3)
    author_names, author_borrow_counts = zip(*top_authors)
    plt.bar(author_names, author_borrow_counts, color='orange')
    plt.title("Top 3 Most Borrowed Authors")
    plt.xlabel("Author")
    plt.ylabel("Number of Loans")
    plt.show()

def plot_loans_over_time(loans):
    """Line chart showing the number of loans over time."""
    loan_dates = [pd.to_datetime(loan.loan_date) for loan in loans]
    loan_df = pd.DataFrame({'Date': loan_dates})
    loan_df['Month'] = loan_df['Date'].dt.to_period('M')
    loans_per_month = loan_df['Month'].value_counts().sort_index()
    loans_per_month.plot(kind='line', marker='o', color='purple')
    plt.title("Number of Loans Over Time")
    plt.xlabel("Month")
    plt.ylabel("Number of Loans")
    plt.show()

# Main logic
with app.app_context():
    print("Fetching data...")
    books, loans, users = fetch_data()

    if not books or not loans or not users:
        print("The database is empty or incomplete. Please populate the database and try again.")
    else:
        print("\n=== Library Statistics ===")
        calculate_statistics(books, loans, users)

        print("\nGenerating visualizations...")
        plot_probability_density(books)
        plot_pages_vs_borrowing_duration(loans)
        plot_top_borrowed_authors(Counter([loan.book.author for loan in loans]))
        plot_loans_over_time(loans)

    print("\nDone.")
