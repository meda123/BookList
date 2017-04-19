# Using BeautifulSoup to scrape online book lists
from bs4 import BeautifulSoup 
import requests 
import bleach 
from model import connect_to_db, User, Lista, List_Book, Book, db

# imports so that I can add to my database 
import server_helper 

# Temporary connection to database to test functions below
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
        list_title = ((bleach.clean((soup.title), tags=[], strip=True)).encode('utf-8')).strip('\n').split(" (")[0]

    
        book_titles = soup.find_all("a", class_="bookTitle")
        book_authors = soup.find_all("a", class_="authorName")
        book_covers = soup.find_all("img", class_="bookSmallImg")


        result = []
        for a, b, c in zip(book_titles, book_authors, book_covers):
            book_title = (bleach.clean(a, tags=[], strip=True)).encode('utf-8').strip('\n')
            book_author = (bleach.clean(b, tags=[], strip=True)).encode('utf-8').strip('\n')
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
    

# # Call scrape_list and pass list url to scrape list 
# scrape_result = scrape_list(" ")
# print scrape_result

# # Call scrape_to_db once you want to add scrape results to database 
# scrape_to_db(scrape_result)
# print "added to db"

             
#Lists to scrape as of 4/18/17 
# https://www.goodreads.com/list/best_of_year/2016 (just this one so far)
# https://www.goodreads.com/list/best_of_year/2015
# https://www.goodreads.com/list/best_of_year/2014
# https://www.goodreads.com/list/best_of_year/2013 
# https://www.goodreads.com/list/best_of_year/2012
# https://www.goodreads.com/list/best_of_year/2006
# https://www.goodreads.com/list/show/550.Best_Love_Stories_
# https://www.goodreads.com/list/show/57.Best_Ever_Contemporary_Romance_Books
# https://www.goodreads.com/list/show/15.Best_Historical_Fiction
# https://www.goodreads.com/list/show/43.Best_Young_Adult_Books
# https://www.goodreads.com/list/show/3.Best_Science_Fiction_Fantasy_Books
# https://www.goodreads.com/list/show/11.Best_Crime_Mystery_Books
# https://www.goodreads.com/list/show/135.Best_Horror_Novels
# https://www.goodreads.com/list/show/281.Best_Memoir_Biography_Autobiography
# https://www.goodreads.com/list/show/29013.Best_Biographies
# https://www.goodreads.com/list/show/8306.Thrillers_You_Must_Read_
# https://www.goodreads.com/list/show/633.Favourite_Travel_Books



















