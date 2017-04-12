""" Booklist App """
import unicodedata

# used for Gooreads API 
import requests 
import xmltodict
from json import dumps
import os
gr_api_key = os.environ['goodreads_key']


# Temporary connection to database to test helper functions 
from flask import Flask, render_template, request, flash, redirect, session
from model import connect_to_db, User, Lista, List_Book, Book, db
app = Flask(__name__)

if __name__ == "__main__":
    connect_to_db(app) 



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

def check_books(book_title, book_author):
    """ This function receives title and author to check given book already 
    exists in the books table, if book is NOT in books table, it is added."""

    # Query to see if the combination of book & author exist in the books table
    title_author_query = Book.query.filter(Book.book_title==book_title, Book.book_author==book_author).all()

    if title_author_query == []:
        return False 
    else: 
        return True  
        
def add_to_books_table(book_title, book_author, book_cover):

    book_to_db = Book(book_title=book_title, book_author=book_author, book_cover=book_cover)
    db.session.add(book_to_db)
    db.session.commit()
    return book_to_db


def add_to_list_book(list_id, book_id):
    book_to_listbook = List_Book(list_id=list_id, book_id=book_id)
    db.session.add(book_to_listbook)
    db.session.commit()




