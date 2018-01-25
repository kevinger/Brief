#Brief#

This is a proof of concept based on research for a 2016 Knight Visiting Nieman Fellowship, focused on machine learning and explanatory journalism. 

The idea is to explore how software might generate background briefs to help journalists, or even initial drafts of explainers.

This code relies on APIs to find quality content on a topic, summarize it, and report on the various sub-topics it includes. The output is an HTML document.

##Required APIs include:##
Bing (search for links)
Diffbot (get article text)
Agolo (summarize articles)
openCalais (get topics and entities)

It requires API keys for all four, and takes as input a topic -- like "income inequality" -- and subheds, areas the journalist is curious to learn more about.

To read more about the origins of this research, go here:
https://hbr.org/2017/07/why-ai-cant-write-this-article-yet
http://www.beyondthetimes.com/wp-admin/post.php?post=1857