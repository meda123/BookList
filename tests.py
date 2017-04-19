import server 
import unittest
# import test_data 

# import server_helper 

# from server import app
# from model import db, example_data, connect_to_db


class MyAppUnitTestCase(unittest.TestCase):
    """ Unit tests for booklist app. """

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True 

    def test_index(self):
        result = self.client.get('/')
        self.assertIn('Welcome to Booklist App', result.data)

    def test_register_form(self):
        result = self.client.get('/register_form')
        self.assertIn('Join a community', result.data)
   

    # DATABASE items to test && remember to test server_helper.py too

    def test_register_input(self):
        pass 

    def test_login_input(self):
        pass 

    def test_logout_page(self):
        """ needs id."""
        pass 


    # """Flask tests that use the database."""
    # def setUp(self):
    #     """ Steps to follow before running every test."""

    #     self.client = app.test_client()
    #     app.config['TESTING'] = True

    #     # Connect to test database (uncomment when testing database)
    #     connect_to_db(app, "postgresql:///testdb")

    #     # Create tables and add sample data (uncomment when testing database)
    #     db.create_all()
    #     example_data()

    # def tearDown(self):
    #     """Do at end of every test."""

    #     # (uncomment when testing database)
    #     db.session.close()
        # db.drop_all()


if __name__ == "__main__":
    unittest.main()



