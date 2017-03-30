""" Booklist App """

from jinja2 import StrictUndefined 

from flask import Flask, render_template, request, flash, redirect, session 
from flask_debugtoolbar import DebugToolbarExtension 

# Imports to use Goodreads API 
import requests 
import xmltodict
from json import dumps

# IMPORT your tables OVER HERE !! 
from model import connect_to_db 

app = Flask(__name__)

# This is required to use my Flask sessions and the debug toolbar 
app.secret_key = "ABC"

#This is in case Jinja2 fails, it will raise an errror, it's default is to fail 
# silently. 
app.jinja_env.undefined = StrictUndefined


#####################################################################
# App routes 

@app.route('/')
def home():
    """ Homepage - where user is asked to login. """

    return render_template("homepage.html")

@app.route('/profile')
def show_profile():
    """ User's profile page, displays lists, logout, and add button."""

    return render_template("profile.html") 

@app.route('/results', methods=["POST"])
def view_results():

    user_search = request.form.get("search_box")
    search_result = query_gr("shonda+rhimes")

    return render_template("results.html", search_result=search_result)

    # return render_template("results.html", find=user_search)


#####################################################################
# Helper functions 

# NOTA: This function returns ONLY the FIRST result 
def query_gr(user_query):

    query_api = requests.get("https://www.goodreads.com/search.xml?key=xPgdvQL3gCl9ImmVLdJ8A&q={0}".format(user_query))

    ## Change xml to ordered dictionary (note ALL results are provided)
    rdict = xmltodict.parse(query_api.content)

    # Parses through intro tags and summaries and takes us to body of results 
    result_body = rdict.get('GoodreadsResponse', 'notfound').get('search', 'notfound1').get('results', 'notfound2').get('work', 'nf3')

    first_result = result_body[0].values()[8].values()

    title = first_result[2] 
    author = first_result[3].values()[1]
    image = first_result[4]

    return ["Title: %s Author: %s Image: %s" % (title, author, image)]



if __name__ == "__main__":
# We have to set debug=True here, since it has to be True at the point
# that we invoke the DebugToolbarExtension
    app.debug = True 

# NOTA: will set up connection to database later
# connect_to_db(app) 

# Use the DebugToolbar
DebugToolbarExtension(app)


app.run(host="0.0.0.0")
