# SCRIPTORIUM - Library Management System

**SCRIPTORIUM** is a comprehensive library management system designed to help manage books, track loans, and generate insightful statistics. This application allows users to view and manage a collection of books, track loan histories, and simulate data for testing purposes.

## Features
- **View and Manage Books**: Easily view the entire collection, including available and borrowed books.
- **Track Loan History**: Track users' borrowing activity and view their loan histories.
- **Generate Statistics**: Get valuable insights like average loan durations, top borrowers, and more.
- **Simulate Data**: Generate test data to simulate book loans, users, and other features.

## Technologies Used
- **Flask**: The web framework powering the application.
- **SQLite**: A lightweight database for storing book, user, and loan data.
- **Bootstrap**: Front-end framework for responsive design.
- **Chart.js**: For generating beautiful, interactive charts for the statistics section.

## Installation Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/amanisakif/Scriptorium-library-management-system.git
   cd scriptorium

### Set up virtual envioronment 
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Activate the virtual environment
source venv/bin/activate

### Run app
python -m flask run

## Open your browser and navigate to: http://127.0.0.1:5000/

### Simulating Data
To simulate books, users, and loans, use the Simulate Data button in the navigation bar. This will reset the database and generate new data.

## Application Routes

- **Home** (`/`): Displays an introduction to the system with features and instructions.
- **All Books** (`/books`): Lists all books in the library, including their status (available/borrowed).
- **Available Books** (`/books/available`): Shows only books that are currently available for borrowing.
- **Borrowed Books** (`/books/borrowed`): Shows books that are currently borrowed.
- **User Loan History** (`/users/<user_id>/loans`): Displays the loan history of a specific user, categorized into current loans (not returned) and past loans (returned).
- **Statistics** (`/statistics`): Displays:
  - Average loans per user.
  - Average loan duration.
  - Top 3 borrowers (with the most loans or longest average loan duration).
  - Borrowing trends visualized as a graph.

## Standalone Descriptive Statistics Script

The `test.py` script allows you to analyze the library data independently, without running the Flask application.

### How to Run the Script
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Run the script with options for statistics and/or plots:
   ```bash
   python test.py --statistics --plots
   ```

### Script Outputs
- **Statistics**:
  1. Author with the most books in the catalog.
  2. Most borrowed author by all users.
  3. Authors exclusively borrowed by each user.
  4. Most borrowed book since the library's opening.
  5. User with the most simultaneous unreturned loans.
- **Plots**:
  1. **Probability Density of Goodreads Ratings**: A histogram showing the distribution of book ratings.
  2. **Pages vs Borrowing Duration**: A scatter plot showing the relationship between book length and borrowing time.


## Database Initialization

To set up the database for the first time:

1. Initialize the database:
   ```bash
   flask db init
   ```

2. Apply migrations:
   ```bash
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

This will create the necessary tables for books, users, and loans.
