class Article(object):

    def __init__(self, url='', title='', text='', topics=[],
                 entities=[], summary='', source=''):
        self.url = url
        self.title = title
        self.text = text
        self.topics = topics
        self.entities = entities
        self.summary = summary
        self.source = source
