# NextRead


NextRead is the 4 week project that I completed during my time as an software engineering fellow at Hackbright. 
NextRead is a reading list and book recommendations site, ideally by knowing what to read next you spend less time finding your
next read and read more books. NextRead is powered by the Typeahead Javascript library and the Goodreads API so that a user 
does not have to spend time remembering book titles/authors and can add a book to their reading list on the go. 

##Contents

Technologies
[Database Model](#database model)
Features
Installation
Technologies

Backend: Python, Flask, PostgreSQL, SQLAlchemy, Beautiful Soup 
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3, Typeahead JS
APIs: Goodreads 


# Features

## Homepage
![alt text](static/images/homepage_rm.png)

## Dashboard
![alt text](static/images/Dashboard_rm.png)
![alt text](static/images/typeahead_rm.png)

## View Lists
![alt text](static/images/list_view_rm.png)

## Installation 

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

https://github.com/meda123/NextRead
Create and activate a virtual environment inside your NextRead directory:

virtualenv env
source env/bin/activate
Install the dependencies:

pip install -r requirements.txt
Sign up to use the Goodreads API (https://www.goodreads.com/api)

Save your API key in a file called secrets.sh using this format:

export APP_ID="YOUR_KEY_GOES_HERE"
Also in secrets.sh add the infomration for the mail server you want to use in this format:

Source your keys from your secrets.sh file into your virtual environment:

source secrets.sh
Set up the database:

python model.py
Run the app:

python server.py
You can now navigate to 'localhost:5000/' to access NextRead.
