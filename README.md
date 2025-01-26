# Scriptorium Library Management System

This project is a Flask-based web application for managing books, users, and loans in a library. The project includes detailed setup instructions, an explanation of the file structure, and guidance on how to run the application. This README has been written to match your code and meet the assessment requirements.

---

## Prerequisites

### Required Software:

1. **Python 3.11**

   - Ensure Python 3.11.x is installed. Check by running:
     ```bash
     python3 --version
     ```
   - If not installed, download from [python.org](https://www.python.org/downloads/).

2. **pip** (comes with Python)

   - Check by running:
     ```bash
     pip --version
     ```

3. **Virtual Environment (venv)**

   - Make sure you can create virtual environments using `venv`.

4. **SQLite** (comes pre-installed with Python).

---

## Project Structure

### Folder and File Overview:

```
scriptorium-library-management-system/
│
├── app/
│   ├── __init__.py       # Initializes the Flask app and database
│   ├── models.py         # Contains database models: Book, User, Loan
│   ├── routes.py         # Defines app routes and business logic
│   ├── forms.py          # Contains WTForms classes for user input validation
│   ├── static/           # Static assets (CSS, JS, images)
│   │   ├── css/
│   │   │   └── styles.css # Main stylesheet for the application
│   │   ├── js/
│   │   │   └── scripts.js # Custom JavaScript functionality
│   │   └── img/          # Images used in the application
│   │       ├── book1.jpg
│   │       ├── book2.jpg
│   │       ├── book3.jpg
│   │       ├── book4.jpg
│   │       └── library-welcome-horizontal.jpg
│   ├── templates/        # HTML templates for rendering views
│       ├── base.html     # Base template for consistent layout
│       ├── index.html    # Homepage template
│       ├── books.html    # Displays book list
│       ├── all_users.html # Displays all users
│       ├── user_loans.html # Displays loans for a specific user
│       └── statistics.html # Displays library statistics
│
├── instance/             # Holds instance-specific data
├── .gitignore            # Specifies files to ignore in version control
├── populate_data.py      # Populates the database with mock data
├── requirements.txt      # Python dependencies with pinned versions
├── run.py                # Main script to run the Flask app
├── test.py               # Script for descriptive statistics and visualizations
└── README.md             # Project documentation (this file)
```

### Key Files and Their Purpose:

1. **`app/__init__.py`**

   - Initializes the Flask app.
   - Configures the SQLite database with URI: `sqlite:///library.db`.
   - Registers the app’s routes from `routes.py`.

2. **`app/models.py`**

   - Defines the database models:
     - **Book**: Represents books with attributes like title, author, pages, etc.
     - **User**: Represents library users.
     - **Loan**: Tracks loans of books by users.

3. **`app/routes.py`**

   - Contains route handlers and logic for the web app.
   - Manages user interactions like viewing books, loans, and users.

4. **`app/forms.py`**

   - Defines forms using Flask-WTF for handling and validating user inputs.

5. **`populate_data.py`**

   - Populates the database with mock data for testing purposes.
   - Adds sample books, users, and loans to the database.

6. **`run.py`**

   - Launches the Flask app and starts the development server.
   - Provides an online navigation interface (menu) to access the following sections:
     - **View Book List**: Displays all books, separating available and borrowed books.
     - **Loan History by User**: Allows users to view their loan history (both returned and unreturned books).
     - **Descriptive Statistics**: Shows average loans per user in 2024 and average loan duration, along with a dynamic graph that toggles between users with the most books borrowed or longest average loan duration.
   - Access the app in the browser at: [http://127.0.0.1:5001/](http://127.0.0.1:5001/).

7. **`test.py`**

   - Python script to calculate descriptive statistics from the loan data.
   - This script runs in the terminal and displays the results of the following descriptive statistics:
     - The author with the most books in the library catalog.
     - The most borrowed author by all users.
     - For each user, the list of authors they have exclusively borrowed.
     - The most borrowed book since the library’s opening.
     - The user with the most simultaneous unreturned loans, showing the dates during which this user had this maximum number of loans.
   - It also produces two visualizations:
     - The estimated probability density of the Goodreads ratings for all the books in the library.
     - A scatter plot representing the linear relationship between the number of pages and the borrowing time of books that have already been borrowed and returned.

8. **`static/`**

   - Contains all static files:
     - CSS: For styling the web pages.
     - JS: For custom JavaScript.
     - Images: Used across the web pages.

9. **`templates/`**

   - Contains HTML templates for rendering pages dynamically.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/amanisakif/scriptorium-library-management-system.git
cd scriptorium-library-management-system
```

### 2. Create and Activate a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all necessary Python packages with version constraints:

```bash
pip install -r requirements.txt
```

#### Required Dependencies:

- **Flask**: `2.2.2`
- **Werkzeug**: `2.2.3`
- **Flask-SQLAlchemy**: `2.5.1`
- **Flask-WTF**: `1.0.1`
- **Flask-Migrate**: `3.1.0`
- **pandas**: `1.5.3`
- **matplotlib**: `3.6.3`
- **numpy**: `1.23.5`
- **SQLAlchemy**: `1.4.47`

### 4. Populate the Database

Run the following script to populate the database with sample data:

```bash
python populate_data.py
```

This step creates mock data for books, users, and loans in the SQLite database (`library.db`).

### 5. Run the Application

Start the Flask development server:

```bash
python run.py
```

The app will be accessible at:

[http://127.0.0.1:5001/](http://127.0.0.1:5001/)

### 6. Run the Test Script

Run the following command to execute the `test.py` script:

```bash
python test.py
```

The script will display the descriptive statistics in the terminal and generate two visualizations saved as image files.

### 7. Verify Installed Versions

To verify the installed versions of all dependencies, use:

```bash
pip show Flask Werkzeug Flask-SQLAlchemy
```

You should see the following versions:

- Flask: `2.2.2`
- Werkzeug: `2.2.3`
- Flask-SQLAlchemy: `2.5.1`

---

## Troubleshooting

1. **Flask Import Errors**:

   - Ensure the virtual environment is activated.
   - Check that all dependencies are installed correctly.
   - Verify the Python version is 3.11.

2. **Dependency Issues**:

   - If `pip install -r requirements.txt` fails, install the packages manually with pinned versions:
     ```bash
     pip install Flask==2.2.2 Werkzeug==2.2.3 Flask-SQLAlchemy==2.5.1 Flask-WTF==1.0.1 Flask-Migrate==3.1.0 pandas==1.5.3 matplotlib==3.6.3 numpy==1.23.5 SQLAlchemy==1.4.47
     ```

3. **Database Not Found**:

   - Ensure `populate_data.py` has been run before starting the app.


