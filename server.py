""" Booklist App """

from jinja2 import StrictUndefined 

from flask import Flask, render_template, request, flash, redirect, session 
from flask_debugtoolbar import DebugToolbarExtension 

# IMPORT your tables OVER HERE !! 
from model import connect_to_db 

app = Flask(__name__)

# This is required to use my Flask sessions and the debug toolbar 
app.secret_key = "ABC"

#This is in case Jinja2 fails, it will raise an errror, it's default is to fail 
# silently. 
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    """ Homepage - where user is asked to login. """

    return render_template("homepage.html")



if __name__ == "__main__":
# We have to set debug=True here, since it has to be True at the point
# that we invoke the DebugToolbarExtension
    app.debug = True 

# NOTA: will set up connection to database later
# connect_to_db(app) 

# Use the DebugToolbar
DebugToolbarExtension(app)


app.run(host="0.0.0.0")
