# Using BeautifulSoup to scrape online book lists
from bs4 import BeautifulSoup 
import requests 
import bleach 
from model import connect_to_db, User, Lista, List_Book, Book, db

# imports so that I can add to my database 
import server_helper 

def scrape_lists(pageurl):
    """ This functon scrapes book title, author, and cover url give a page url
    and adds scraped information to the books, pl_books, public_lists tables. """

    for page in range(1,2):
        url = "{}".format(pageurl)
        r = requests.get(url)

        data = r.text 
        soup = BeautifulSoup(data, "lxml")

        # Bleach sanitizes an item by removing tags and/or attributes 
        list_title = (bleach.clean((soup.title), tags=[], strip=True)).encode('utf-8')
        print list_title
    
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
        
        return result


test = scrape_lists("https://www.goodreads.com/list/show/110568.Parenting_a_Gifted_Child")
print test 





