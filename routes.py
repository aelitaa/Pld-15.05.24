from flask import Blueprint, request, jsonify
from app import db
from models import Book
from flask_jwt_extended import jwt_required

book_blueprint = Blueprint('books', __name__)

@book_blueprint.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@book_blueprint.route('/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

@book_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        publication_date=data['publication_date'],
        genre=data['genre'],
        isbn=data['isbn']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@book_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    book.publication_date = data['publication_date']
    book.genre = data['genre']
    book.isbn = data['isbn']
    db.session.commit()
    return jsonify(book.to_dict())

@book_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

