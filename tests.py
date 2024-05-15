import unittest
from app import app, db
from models import Book, User
from flask_jwt_extended import create_access_token

class BookTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()
        self.create_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_user(self):
        user = User(username='testuser', password=generate_password_hash('testpass', method='sha256'))
        db.session.add(user)
        db.session.commit()

    def get_auth_token(self):
        response = self.app.post('/api/auth/login', json={'username': 'testuser', 'password': 'testpass'})
        return response.get_json()['access_token']

    def test_add_book(self):
        token = self.get_auth_token()
        response = self.app.post('/api/books/', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_date': '2023-05-15',
            'genre': 'Test Genre',
            'isbn': '1234567890'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        response = self.app.get('/api/books/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

