from keys import *
import httplib, urllib, base64, json
import requests, json

import nltk
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

def remove_stop_words(tokens):
    #Takes a list of words, remove common ones
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in tokens if w.lower() not in stopwords]
    return content

def similarity(doc1,doc2):
    #Takes two strings, returns cosine similarity
    vect = TfidfVectorizer()
    docs = [doc1,doc2]
    tfidf = vect.fit_transform(docs)
    similarity = (tfidf * tfidf.T).A
    return similarity[1][0]

def stem_and_stop(doc):
    #Tokenize, stem words, remove stop words
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(doc)
    tokens = remove_stop_words(tokens)
    ps = PorterStemmer()
    tokens = [ps.stem(t) for t in tokens]

    #Recombine into a string
    content = ' '.join(tokens).lower()
    return content


def articleCounter(articles):
    #Takes a list of Article objects, returns lists of topics and entities
    all_topics = []
    all_entities = []
    all_sources = []
    for a in articles:
        for b in a.topics:
            if b not in all_topics:
                all_topics.append(b)
        for c in a.entities:
            if c not in all_entities:
                all_entities.append(c)
        if a.source not in all_sources:
            all_sources.append(a.source)
    return all_topics, all_entities, all_sources

def openCalais(access_token, text):
    #Takes text, saves it to a file,
    #then sends file to openCalais API to get topics
    try:
        #Remove non-utf-8 characters
        text = text.encode('utf-8').strip()
        #Save text to file
        text_file = open("openCalais.txt", "w")
        text_file.write(text)
        text_file.close()

        #Text file to API
        headers = {'X-AG-Access-Token' : access_token, 'Content-Type' : 'text/raw',
                   'outputformat' : 'application/json', 'omitOutputtingOriginalText' : 'True',
                   'x-calais-language' : 'English'}
        calais_url = 'https://api.thomsonreuters.com/permid/calais'
        file_name = "openCalais.txt"
        files = {'file': open(file_name, 'rb')}
        response = requests.post(calais_url, files=files, headers=headers, timeout=80)
        response = response.text
        response = json.loads(response)

        #Get social tags
        social_tags = []
        for a in response.keys():
            if "SocialTag" in a:
                social_tags.append(a)

        topics = []
        for b in social_tags:
            name = str(response[b]['name'])
            importance = int(response[b]['importance'])
            #If importance is high, record topic
            if importance == 1:
                topics.append(name)

        #Get entities
        entities = []
        for b in response.keys():
            try:
                if response[b]['_typeGroup'] == 'entities' and response[b]['relevance'] > .5:
                    entities.append(response[b]['name'])
            except:
                continue

        return topics, entities

    except:
        print "Error with openCalais"
        return [],[]

def agolo(key,num_sentences,title,text):
    #Takes a key, a number of sentences, a headline and text. Returns Agolo summary object
    #Documentation: https://dev.agolo.com/docs/services/570d7b4f88b6e5116cdf6a17/operations/570d7b5188b6e508dcfb1c90

    body = {
        "summary_length": num_sentences,
        "articles": [{
            "type": "article",
            "title": title,
            "text": text
            }]
        }

    body = json.JSONEncoder().encode(body)


    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('api.agolo.com')
        conn.request("POST", "/nlp/v0.2/summarize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return "Error"



def diffbot(url,key):
    #Takes a URL and Diffbot API key; returns url plus title and text
    #Documentation: https://www.diffbot.com/dev/docs/article/

    endpoint = 'https://api.diffbot.com/v3/article?' + 'token=' + key + '&url='

    result = requests.get(endpoint + url)
    result = json.loads(result.text)

    try:
        title = result['objects'][0]['title']
    except:
        title = "NA"

    try:
        text = result['objects'][0]['text']
    except:
        text = "NA"

    content = [url,title,text]

    return content

def bing(key,term,number_of_results,offset,news=False,sites=[]):
    #Takes a search term, number of results, offset
    #News = True means a Bing news search, else web search
    #Returns list of urls
    #Documentation: https://dev.cognitive.microsoft.com/docs/services

    count = 0
    sites_string = ' ('
    if len(sites) > 0:
        while count < len(sites):
            if count == len(sites) - 1:
                site = 'site:'+str(sites[count])
                sites_string = sites_string + site
            else:
                site = 'site:'+str(sites[count])+' OR '
                sites_string = sites_string + site
            count +=1
        term = term + sites_string

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': key,
    }

    params = urllib.urlencode({
        # Request parameters
        'q': term,
        'count': number_of_results,
        'offset': offset,
        'mkt': 'en-us',
        'safeSearch': 'Moderate'
        #'freshness': 'Month'
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        if news == True:
            conn.request("GET", "/bing/v7.0/news/search?%s" % params, "{body}", headers)
        else:
            conn.request("GET", "/bing/v7.0/search?%s" % params, "{body}", headers)

        response = conn.getresponse()
        data = response.read()
        conn.close()
        results = json.loads(data)
        #Return articles
        articles = []
        count = 0

        while count < number_of_results:
            if news == True:
                url = results['value'][count]['url']
            else:
                url = results['webPages']['value'][count]['url']
            articles.append(url)
            count +=1
        return articles
    except Exception as e:
        return e
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def google(term):
    # https://developers.google.com/custom-search/docs/start
    # https://google-api-client-libraries.appspot.com/documentation/customsearch/v1/python/latest/index.html
    service = build("customsearch", "v1", developerKey="AIzaSyBSCEKKW2DB05yJhAa7IhiFv_1Ww01wRU8")

    res = service.cse().list(
        q=term,
        cx='013679191244934975269:vjsjeuddshy'
    ).execute()

    articles = []

    for item in res['items']:
        articles.append(item['link'])
        # print "{}: {}".format(item['title'], item['link'])

    return articles
