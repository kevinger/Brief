from utilities import *
from keys import *
from sources import sites
from model import Article
import time
from jinja2 import Template
from report import report
from urlparse import urlparse
import codecs


#Pick a topic to generate a brief about
term = "income inequality"

#Pick sub-topics
subheds = ['Causes',
           'Globalization and trade',
           'Digital technology and robotics',
           'Taxes',
           'Monopoly and industry concentration',
           'Skills and education',
           'Policies to address inequality']

#Search Bing for links from reliable sources
print "Searching for links to evaluate..."
# links = bing(bing_key,term,20,0,news=False,sites=sites)
links = google(term)

#Get article text for each link
print "Getting text from Diffbot..."
all_content = []
for link in links:
    content = diffbot(link,diffbot_key)
    #Don't include pdfs or cases where no text came through
    if len(content[2]) > 500 and 'pdf' not in content[0]:
        article = Article(url=content[0],title=content[1],
                          text=content[2])
        all_content.append(article)

#Set source for each article
for a in all_content:
    a.source = urlparse(a.url).netloc

#Get summary for each link
print "Getting summaries from Agolo..."
count = 0
for article in all_content:
    count += 1
    print count
    summary = agolo(agolo_key,5,article.title,article.text)
    try:
        summary = eval(summary)
        summary = summary['summary'][0]['sentences']
        final_summary = ''
        for sentence in summary:
            final_summary = final_summary + sentence + ' '
        article.summary = final_summary.decode('ascii','ignore')
    except:
        print "Error converting summary."
        all_content.remove(article)
    #API is rate limited to 5 calls/min https://dev.agolo.com/products/570d737791554004a7060001
    time.sleep(15)

#For each article, get topics and entities
print "Getting topics and entities from openCalais..."
for article in all_content:
    calais = openCalais(calais_token,article.text)
    article.topics = calais[0]
    article.entities = calais[1]

#Get lists of all topics and entities
lists = articleCounter(all_content)
all_topics = lists[0]
all_entities = lists[1]
all_sources = lists[2]

#Get corresponding articles for each topic
articles_by_topic = {}
for topic in all_topics:
    articles = []
    for article in all_content:
        if topic in article.topics:
            articles.append(article)
    articles_by_topic[topic] = articles

#Get corresponding articles for each entity
articles_by_entity = {}
for entity in all_entities:
    articles = []
    for article in all_content:
        if entity in article.entities:
            articles.append(article)
    articles_by_entity[entity] = articles

#Get corresponding articles for each source
articles_by_source = {}
for source in all_sources:
    articles = []
    for article in all_content:
        if source == article.source:
            articles.append(article)
    articles_by_source[source] = articles

#Get most similar summary for each question
subheds_with_similar = []
for s in subheds:
    top_similarity = 0
    best_answer = 'NA'
    clean_sub = stem_and_stop(s)
    for article in all_content:
        all_text = article.summary + article.title + article.title + ' '.join(article.topics)
        all_text = stem_and_stop(all_text)
        score = similarity(clean_sub,all_text)
        if score > top_similarity:
            top_similarity=score
            best_answer = article
    subheds_with_similar.append([s,best_answer,top_similarity])


#Fill html template with data
html = Template(report)
output = html.render(term=term,top_content=all_content[0:3],
                     all_topics=all_topics,all_entities=all_entities,
                     all_sources=all_sources,
                     articles_by_topic=articles_by_topic,
                     articles_by_entity=articles_by_entity,
                     articles_by_source=articles_by_source,
                     subheds_with_similar=subheds_with_similar)
#Save results
save_name = "Results for " + term + ".html"
with codecs.open(save_name, "w", encoding='utf-8') as tk:
    tk.write(output)
