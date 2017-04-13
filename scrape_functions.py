# Using BeautifulSoup to scrape online book lists
from bs4 import BeautifulSoup 
import requests 
import bleach 
from model import connect_to_db, User, Lista, List_Book, Book, db

# imports so that I can add to my database 
import server_helper 

# Temporary connection to database to test helper functions 
from flask import Flask, render_template, request, flash, redirect, session
from model import connect_to_db, User, Lista, List_Book, Book, PL_Book, Public_List, db
app = Flask(__name__)

if __name__ == "__main__":
    connect_to_db(app) 


def scrape_list(pageurl):
    """ This functon scrapes book title, author, and cover url. It saves output
    in a tuple that holds the title and a list containing each book."""

    for page in range(1,2):
        url = "{}".format(pageurl)
        r = requests.get(url)

        data = r.text 
        soup = BeautifulSoup(data, "lxml")

        # Bleach sanitizes an item by removing tags and/or attributes 
        list_title = (bleach.clean((soup.title), tags=[], strip=True)).encode('utf-8')
    
        book_titles = soup.find_all("a", class_="bookTitle")
        book_authors = soup.find_all("a", class_="authorName")
        book_covers = soup.find_all("img", class_="bookSmallImg")


        result = []
        for a, b, c in zip(book_titles, book_authors, book_covers):
            book_title = (bleach.clean(a, tags=[], strip=True)).encode('utf-8')
            book_author = (bleach.clean(b, tags=[], strip=True)).encode('utf-8')
            book_cover = c['src']
            book_attributes = (book_title,book_author, book_cover)
            result.append(book_attributes)
        
        return (list_title, result)


def scrape_to_db(scrape_result):
    """ This functon uses the scrape results and adds the list title to the 
    database, and loops through each book inside the list to see if book should
    be added to the database."""

    plist_name = scrape_result[0]
    all_books = scrape_result[1]
    plist_check = server_helper.check_public_list(plist_name)

    if plist_check:
        print "Since on DB, don't go any further."

    else:  
        server_helper.add_to_public_list(plist_name)
        print "new list added to DB & now ADD books" 

        # Start looping through each book in list: check title & author before adding to DB
        book_order = 0
        for book in all_books: 
            title = book[0] 
            author = book[1]
            cover = book[2]
            book_order = 1 + book_order 

            # Function below checks in book exists in database 
            book_in_db = server_helper.check_books(title, author)

            # If book exists in books table, only add to pl_books table to capture book_order 
            if book_in_db:
                pl_id = Public_List.query.filter(Public_List.pl_name == plist_name).first().pl_id
                book_id = Book.query.filter(Book.book_title == title).first().book_id
                add_pl_table = server_helper.add_to_pl_book(book_id, pl_id, book_order)
            

            # Book not found? Add to books table & pl_books table     
            else: 
                new_book = server_helper.add_to_books_table(title, author, cover)
                new_book_id = new_book.book_id  
                pl_id = Public_List.query.filter(Public_List.pl_name == plist_name).first().pl_id  
                add_pl_table = server_helper.add_to_pl_book(new_book_id, pl_id, book_order)
    

# CALL scrape_list and pass list url to scrape the list 
# scrape_result = scrape_list("https://www.goodreads.com/list/show/13601.Goodreads_Filipino_Group_Favorite_Mystery_Thriller_Books")
# scrape_to_db(scrape_result)
# print "Added to DB -- now check lol"

             

         

















