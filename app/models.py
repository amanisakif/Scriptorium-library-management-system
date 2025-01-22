from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), default="available")
    pages = db.Column(db.Integer, nullable=False)
    goodread_rating = db.Column(db.Float, nullable=False)

    loans = db.relationship('Loan', back_populates='book')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    loans = db.relationship('Loan', back_populates='user')

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.String(10), nullable=False)
    return_date = db.Column(db.String(10), nullable=True)

    user = db.relationship('User', back_populates='loans')
    book = db.relationship('Book', back_populates='loans')
