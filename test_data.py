import unittest, sys, os

sys.path.append('..')
from main import app, db

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    ###############
    #### tests ####
    ###############

    def register(self, email, password):
        return self.app.post('/register',
                            data=dict(email=email,
                                      password=password, 
                                      confirm_password=password),
                            follow_redirects=True)

    def test_valid_user_registration(self):
        response = self.register( 'test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_username_registration(self):
        response = self.register('test@example.com', 'FlaskIsAwesome')
        self.assertNotEqual(response.status_code, 300)
        
    def test_invalid_email_registration(self):
        response = self.register('test@example', 'FlaskIsAwesome')
        self.assertIn(b'Invalid email address.', response.data)
        self.assertNotEqual(response.status_code, 300)

if __name__ == "__main__":
    unittest.main()