report = '''<!DOCTYPE html>
<html>
  <head>
  <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{term}} -- Briefing</title>
    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
     <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
  <div class="container-fluid">
  <h1>A Brief on {{term}}</h1>
  {% for s in subheds_with_similar %}
    <h2>{{s[0]}}</h2>
    <h3><a href="{{s[1].url}}">{{s[1].title}}</a></h3>
    <b>{{s[1].source}}</b>
    <p>{{s[1].summary}}</p>
  {% endfor %}
  <h2>Topics</h2>
  {% for topic in all_topics %}
      <li><a href="#{{topic}}">{{ topic }}</a></li>
  {% endfor %}
  <h2>Entities</h2>
  {% for entity in all_entities %}
      <li><a href="#{{entity}}">{{ entity }}</a></li>
  {% endfor %}
  <h2>Sources</h2>
  {% for source in all_sources %}
      <li><a href="#{{source}}">{{ source }}</a></li>
  {% endfor %}
  <h2>Summaries by topic</h2>
  {% for topic in articles_by_topic.keys() %}
     <h3 id="{{topic}}">{{ topic }}</h3>
     {% for article in articles_by_topic[topic] %}
         <h3><a href="{{ article.url }}">{{ article.title }}</a></h3>
         <b>{{article.source}}</b>
         <p>{{ article.summary }}</p>
     {% endfor %}
   {% endfor %}
  <h2>Summaries by entity</h2>
  {% for entity in articles_by_entity.keys() %}
     <h3 id="{{entity}}">{{ entity }}</h3>
     {% for article in articles_by_entity[entity] %}
         <h3><a href="{{ article.url }}">{{ article.title }}</a></h3>
         <b>{{article.source}}</b>
         <p>{{ article.summary }}</p>
     {% endfor %}
   {% endfor %}
  <h2>Summaries by source</h2>
  {% for source in articles_by_source.keys() %}
     <h3 id="{{source}}">{{ source }}</h3>
     {% for article in articles_by_source[source] %}
         <h3><a href="{{ article.url }}">{{ article.title }}</a></h3>
         <b>{{article.source}}</b>
         <p>{{ article.summary }}</p>
     {% endfor %}
   {% endfor %}
  </div>
  </body>'''
