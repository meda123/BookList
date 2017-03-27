""" Models and databse functions for Booklist App """

from flask_sqlalchemy import SQLAlchemy 

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)


db = SQLAlchemy()


#####################################################################
# Model definitions 
# NOTA: Will add this once I have my database model approved 




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