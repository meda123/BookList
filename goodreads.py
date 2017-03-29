import requests 
import xmltodict
from json import dumps

# Test 1: Ender's game 
# r = requests.get("https://www.goodreads.com/search.xml?key=xPgdvQL3gCl9ImmVLdJ8A&q=Ender%27s+Game")


trythis = 'Shonda+rhimes'

# '{} {}'.format('one', 'two')

# Request to API sends us XML, hard coded value rn NOTA 
r = requests.get("https://www.goodreads.com/search.xml?key=xPgdvQL3gCl9ImmVLdJ8A&q={0}".format(trythis))

# Change xml to ordered dictioanary (note ALL results are provided)
rdict = xmltodict.parse(r.content)

# Parses through intro tags and summaries and takes us to body of results 
result_body = rdict.get('GoodreadsResponse', 'notfound').get('search', 'notfound1').get('results', 'notfound2').get('work', 'nf3')

# Book info for second result 
first_result = result_body[0].values()[8].values()
title = first_result[2]
print title
author = first_result[3].values()[1] 
print author
image = first_result[4]
print image 

# Book info for second result 
second_result = result_body[1].values()[8].values()
title2 = second_result[2]
print title2
author2 = second_result[3].values()[1] 
print author2
image2 = second_result[4]
print image2 

# Book info for second result 
second_result = result_body[1].values()[8].values()
title2 = second_result[2]
print title2
author2 = second_result[3].values()[1] 
print author2
image2 = second_result[4]
print image2 


# def show_books(trythis):












