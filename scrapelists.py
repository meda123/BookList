from bs4 import BeautifulSoup 
import requests 
import bleach 

# Using BeautifulSoup to scrape online book lists

# Only want to scrape for the first page of the website 
for page in range(1,2):
    url = "https://www.goodreads.com/list/show/110568.Parenting_a_Gifted_Child".format(page)
    r = requests.get(url)

    data = r.text 
    soup = BeautifulSoup(data, "lxml")

    # Bleach sanitizes an item by removing tags and/or attributes 
    list_title = bleach.clean((soup.title), tags=[], strip=True)
    print list_title
    
    book_titles = soup.find_all("a", class_="bookTitle")
    book_authors = soup.find_all("a", class_="authorName")
    book_covers = soup.find_all("img", class_="bookSmallImg")

    test = len(book_titles)
    print test 

    result = []
    for a, b, c in zip(book_titles, book_authors, book_covers):
        book_title = (bleach.clean(a, tags=[], strip=True)).encode('utf-8')
        book_author = (bleach.clean(b, tags=[], strip=True)).encode('utf-8')
        book_cover = c['src']
        book_attributes = (book_title,book_author, book_cover)
        result.append(book_attributes)
    print result





