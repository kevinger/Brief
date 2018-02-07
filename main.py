from utilities import *
from keys import *
from sources import sites
from model import Article
import time
from jinja2 import Template
from report import report
from urlparse import urlparse
import codecs

import pdb

#Pick a topic to generate a brief about
term = "income inequality"

#Search Bing for links from reliable sources
print "Searching for links to evaluate..."
links = google(term,3)

#Get article text for each link
print "Getting summary..."
articles = []
for link in links:
    articles.append(algorithmia(link))

pdb.set_trace()
