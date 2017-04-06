""" Booklist App """
import unicodedata

# used for Gooreads API 
import requests 
import xmltodict
from json import dumps
import os

gr_api_key = os.environ['goodreads_key']

from jinja2 import StrictUndefined 

from flask import Flask, render_template, request, flash, redirect, session 
from flask_debugtoolbar import DebugToolbarExtension 


from model import connect_to_db, User, Lista, List_Book, Book, db
# from functiongr import query_gr

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

    flash("User %s added, please login with your credentials" % name)
    return redirect("/users/%s" % new_user.user_id)

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
    user_lists = Lista.query.filter(Lista.user_id == user_id).all()
     
    return render_template("user.html", user=user, user_lists=user_lists)


@app.route('/add_list', methods=['POST'])
def process_list():
    """ If user is logged in, allow them to select a list."""

    user_id = session.get("user_id")

    if user_id:
        list_name = request.form["list_name"] 
        new_list = Lista(list_name=list_name, user_id=user_id)
        db.session.add(new_list)
        db.session.commit()

    else:
        list_name = None


    flash("List added")
    return redirect("/users/%s" %user_id)



@app.route('/view_list', methods=['POST'])
def select_list():
    """If user is logged in and selected a list, let them view that list's details."""
    
    user_id = session.get("user_id") 
    list_name = request.form["list-name"] 
    list_id = Lista.query.filter_by(list_name=list_name).first().list_id
    
    return redirect("/view_list/%s" % list_id)


@app.route("/view_list/<int:list_id>")
def list_details(list_id):

    user = Lista.query.get(list_id).user_id
    list_name = Lista.query.get(list_id).list_name

    return render_template("view_list.html", list_name=list_name)


@app.route('/add_book', methods=['POST'])
def add_book():
    """ If user us logged in, allow them to add a book to a list."""
    user_id=session.get("user_id")

    if user_id:
        # Collect info from the API results (to check against books table)
        book_title = request.form.get("title")
        book_author = request.form.get("author")
        book_cover = request.form.get("cover")

        # Query to see if the combination of book & author exist in the books table
        title_author_query = Book.query.filter(Book.book_title==book_title, Book.book_author==book_author).all()
        list_name = request.form.get("list-name")
        list_id = Lista.query.filter(Lista.list_name == '{}'.format(list_name)).first().list_id

        # If book doesn't exist in books table, add to books table and to list
        if title_author_query == []:
            book_to_db = Book(book_title=book_title, book_author=book_author, book_cover=book_cover)
            db.session.add(book_to_db)
            db.session.commit()

            # Collect info to add to the list_books table
            new_book_id = book_to_db.book_id
            book_to_listbook = List_Book(list_id=list_id, book_id=new_book_id)
            db.session.add(book_to_listbook)
            db.session.commit()

        else: 
            # Book exists in books table, so only add to list_books table 
            book_id = Book.query.filter(Book.book_title == '{}'.format(book_title)).first().book_id
            book_to_listbook = List_Book(list_id=list_id, book_id=book_id)
            db.session.add(book_to_listbook)
            db.session.commit()

    else:
        new_book = None 

    flash("Book added to [add list name]")
    return redirect("/users/%s" %user_id)



@app.route('/results', methods=["POST"])
def view_results():
    """ Allows user to search books to add them to a list."""

    user_search = request.form.get("search_box")
    search_result = query_gr("%s" % user_search)

    user_id=session.get("user_id")

    user_lists = Lista.query.filter(Lista.user_id == user_id).all()

    return render_template("results.html", user_search=user_search, search_result=search_result, user_lists=user_lists)



#####################################################################
# Helper functions 

def query_gr(user_query):
    """ This function sends an search request to the Goodreads API, we receive the
    top 20 results associated with key words (author, title, isbn)."""
    
    query_api = requests.get("https://www.goodreads.com/search.xml?key={}&q={}".format(gr_api_key, user_query))

    ## Change xml to ordered dictioanary (note ALL results are provided)
    rdict = xmltodict.parse(query_api.content)

    # Parses through intro tags and summaries and takes us to body of results 
    result_body = rdict.get('GoodreadsResponse', 'notfound').get('search', 'notfound1').get('results', 'notfound2').get('work', 'nf3')

    result= {}
    for i in range(0,6):

        first_result = result_body[i].values()[8].values()

        titles = first_result[2] 
        authors = first_result[3].values()[1]
        images = first_result[4]
        outputs = (titles, authors, images)
        result[i] = outputs 


    return result


if __name__ == "__main__":
# We have to set debug=True here, since it has to be True at the point
# that we invoke the DebugToolbarExtension
    app.debug = True 

# NOTA: will set up connection to database later
    connect_to_db(app) 

# Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(host="0.0.0.0", debug=True)
