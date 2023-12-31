import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import *


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        # db.init_app(self.app)
        self.client = self.app.test_client
        self.db=db
        # self.database_name = "bookshelf_test"
        # self.database_path = "postgresql://{}:{}@{}/{}".format(
        #     "student", "student", "localhost:5432", self.database_name

        # )
        # setup_db(self.app, self.database_path)
        # self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aashishraj:123@localhost:5432/bookshelf'
        # self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # db.init_app(self.app)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        # with self.app.app_context():
        #     # self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
    def test_422_on_delete_non_existant_book(self):
        res = self.client().delete("/books/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"unprocessable")

    def test_405_on_delete_when_no_record_is_specified(self):
        res = self.client().delete("/books")
        data = json.loads(res.data)

        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Method Not Allowed")
        self.assertEqual(res.status_code,405)

    def test_405_on_get_a_non_existant_book(self):
        res = self.client().get("/books/1000")
        data = json.loads(res.data)

        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Method Not Allowed")
        self.assertEqual(res.status_code,405)


    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/books?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_200_sent_posting_a_new_book(self):
        newBook = {
            "title":"Annasi Boys",
            "author":"Neil Gaiman",
            "rating":5
        }
        res = self.client().post("/books",json=newBook)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["books"])
        self.assertTrue(data["total_books"])
        self.assertTrue(data["created"])


    def test_get_paginated_books(self):
        res = self.client().get("/books")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))


    def test_200_sent_requesting_from_valid_page(self):
        res = self.client().get("/books?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # self.assertEqual(data["message"], "resource not found")

    # need to test on an existing record
    def test_200_deleting_existing_record(self):
        bookId = 9
        res = self.client().delete("/books/"+str(bookId))
        data = json.loads(res.data)

        book = Book.query.filter(Book.id==bookId).one_or_none()

        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertEqual(data["deleted"],bookId)
        self.assertTrue(data["books"])
        self.assertTrue(data["total_books"])
        self.assertEqual(book,None)

    # need to test on an existing record
    def test_200_on_updating_rating_on_existing_book(self):
        bookId = 11
        rating = 1
        res = self.client().patch("/books/"+str(bookId),json={"rating":rating})
        data = json.loads(res.data)

        book = Book.query.filter(Book.id == bookId).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertEqual(book.format()["rating"], rating)

    # def tearDown(self):
    #     """Executed after reach test"""
    #     pass
    # def test_get_paginated_books(self):
    #     res = self.client().get("/books")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_books"])
    #     self.assertTrue(len(data["books"]))
    #
    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get("/books?page=1000", json={"rating": 1})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")
    #
    # def test_update_book_rating(self):
    #     res = self.client().patch("/books/5", json={"rating": 1})
    #     data = json.loads(res.data)
    #     book = Book.query.filter(Book.id == 5).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(book.format()["rating"], 1)
    #
    # def test_400_for_failed_update(self):
    #     res = self.client().patch("/books/5")
    #
    #
    #     if res.status_code == 200:
    #         data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 415)
    #     # self.assertIsNotNone(data)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "bad request")
    #
    # def test_create_new_book(self):
    #     res = self.client().post("/books", json=self.new_book)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["created"])
    #     self.assertTrue(len(data["books"]))
    #
    # def test_405_if_book_creation_not_allowed(self):
    #     res = self.client().post("/books/45", json=self.new_book)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "method not allowed")
    #
    # # Delete a different book in each attempt
    # def test_delete_book(self):
    #     res = self.client().delete("/books/2")
    #     data = json.loads(res.data)
    #
    #     book = Book.query.filter(Book.id == 2).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 2)
    #     self.assertTrue(data["total_books"])
    #     self.assertTrue(len(data["books"]))
    #     self.assertEqual(book, None)
    #
    # def test_422_if_book_does_not_exist(self):
    #     res = self.client().delete("/books/1000")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")


# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
