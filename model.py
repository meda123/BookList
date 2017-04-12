""" Models and databse functions for Booklist App """

from flask_sqlalchemy import SQLAlchemy 

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions 

class User(db.Model):
    """ User of booklist app. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    last = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=True)
    password = db.Column(db.String(60), nullable=True)
    goodreads_id = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        """Helpful representation when printed."""
        return "<User user_id=%s name=%s> email=%s" % (self.user_id,
                                               self.name, self.email)

class Lista(db.Model):
    """List belonging to each user."""

    __tablename__ ="lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #define relationship to user
    user = db.relationship("User", backref=db.backref("lists",order_by=list_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        m = "<Lista list_id=%s list_name=%s user_id=%s>"
        return m %(self.list_id, self.list_name, self.user_id)


class List_Book(db.Model):
    """Association table connects lists table to books table"""


    __tablename__ = "list_books"

    list_book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    sequence = db.Column(db.Integer, nullable=True)
    book_read = db.Column(db.Boolean, nullable=False, default=False)

    #define relationships to Book 
    book = db.relationship("Book", backref=db.backref("list_books",order_by=list_book_id))
    
    #define relationships to Lista 
    lista = db.relationship("Lista", backref=db.backref("list_books",order_by=list_book_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        m = "<List_Book list_book_id=%s list_id=%s book_id=%s>"
        return m %(self.list_book_id, self.list_id, self.book_id)


class Book(db.Model):
    """Book on the booklist app."""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_title = db.Column(db.String (200), nullable=True)
    book_author = db.Column(db.String (200), nullable=True)
    book_author_2 = db.Column(db.String(200), nullable=True)
    book_cover = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        m = "<Book book_id=%s book_title=%s book_author=%s book_cover=%s >"
        return m %(self.book_id, self.book_title, self.book_author, self.book_cover)


class PL_Book(db.Model):
    """ Association table connects public_list_books table to books table."""

    __tablename__ = "pl_books"

    pl_book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    pl_id = db.Column(db.Integer,db.ForeignKey('public_lists.pl_id'))
    order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        m = "<PL_Book pl_book_id=%s book_id=%s pl_id=%s order=%s >"
        return m %(self.pl_book_id, self.book_id, self.pl_id, self.order)


    #define relationships to Book 
    book = db.relationship("Book", backref=db.backref("pl_books",order_by=pl_book_id))

     #define relationships to Public_List
    public_list = db.relationship("Public_List", backref=db.backref("public_lists",order_by=pl_book_id))



class Public_List(db.Model):
    """ Public list on the booklist app."""
    __tablename__ = "public_lists"

    pl_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pl_name = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        m = "<Public_List pl_id=%s pl_name=%s >"
        return m %(self.pl_id, self.pl_name)
    

#####################################################################
# Helper functions
def connect_to_db(app):
    """ Connect the database to my Flask app."""

    #Configure to use PostgreSQL database   
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///booklist'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if I run this module interactively, it will
    # leave me in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

