""" Booklist App """

from jinja2 import StrictUndefined 

from flask import Flask, render_template, request, flash, redirect, session 
from flask_debugtoolbar import DebugToolbarExtension 

# Need these to interpret Goodreads API response  
import requests 
import xmltodict
from json import dumps


from model import connect_to_db, User, List, List_Book, Book, db

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
    """ Homepage - where user is asked to login or sing-up. """

    return render_template("homepage.html")

@app.route('/register_form', methods = ['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")

@app.route('/register_form', methods=['POST'])
def register_process():
    """ Process registration."""

    # Get form variables
    name = request.form["name"]
    last = request.form["last"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(name=name, last=last, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.user_id 

    flash("User %s added" % name)
    return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_process():
    """ Process login."""

    #Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/users/<int:user_id>")
def user_details(user_id):
    """ Show info about user, displays reading lists, and add book button."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route('/add_list', methods=['POST'])
def process_list():
    """ If user is logged in, let them add/edit a list."""

    user_id=session.get("user_id")

    if user_id:
        list_name = request.form["list_name"] 
        new_list = List(list_name=list_name, user_id=user_id)
        db.session.add(new_list)
        db.session.commit()

    else:
        list_name = None


    flash("List added")
    return redirect("/users/%s" %user_id)







@app.route('/results', methods=["POST"])
def view_results():
    """ Allows user to search books to add them to a list."""

    user_search = request.form.get("search_box")
    search_result = query_gr("%s" % user_search)

    return render_template("results.html", user_search=user_search, search_result=search_result)

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
    connect_to_db(app) 

# Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(host="0.0.0.0")
