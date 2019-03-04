from utilities import google, algorithmia
# from keys import *
from sources import sites
from model import Article
from jinja2 import Template
from report import report
from urlparse import urlparse

import sys, time, codecs

# import pdb

#Pick a topic to generate a brief about
search_term = str(sys.argv[1])
print "\n\tSearch Term: {}\n".format(search_term)

#Search Bing for links from reliable sources
print "Searching for links to evaluate..."
links = google(search_term, 3)

# #Get article text for each link
print "Getting summary..."
articles = []
for link in links:
    articles.append(algorithmia(link))
    print link

if articles:
    for article in articles:
        print " {}".format(article.url)
        print " {}".format(article.title)
        print " {}".format(article.summary.encode('utf-8'))
        print "\n\t----------------------\n"
else:
    print "Error, sort of: no articles found for '{}'?".format(search_term)

# pdb.set_trace()
