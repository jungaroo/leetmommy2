# Leetmommy 2.0

Leetmommy is an open source search engine JSON API backed by ElasticSearch (7.5.1) and scrapy for Rithm school lectures.

Here's a demo frontend app using the Leetmommy 2.0 API
[leetmommy.surge.sh](leetmommy.surge.sh)

# API Documentation

  todo

# Installation (for development)

## Step 1 - Activate environment and download necessary files
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set FLASK_ENV to 'development'

Download Elasticsearch & Kibana: (Works with version 7.5.1)
https://www.elastic.co/downloads/elasticsearch

(Works with version 7.5.1)
https://www.elastic.co/downloads/kibana

## Step 2 - Start servers running
```
# cd into your elastic search directory
cd elasticsearch-*
bin/elasticsearch

# windows:
bin\elasticsearch.bat) 
```
Defaults to port 9200

(Optional) Start up kibana for its development console.
```
# cd into your kibana directory
cd kibana-*
bin/kibana 
# windows:
(bin\kibana.bat)
```
On port 5601

Start flask server
```
flask run
```

Open on localhost:5000

# Tests

```
python3 -m unittest
```
todo



# Extra reading

The old [leetmommy](https://github.com/odoland/leetmommy11) source code

Fuzzy matching - [Levenshtein Edit Distance](https://en.wikipedia.org/wiki/Levenshtein_distance)

Google's paper on [Anatomy of the Search Engine](http://infolab.stanford.edu/~backrub/google.html)

Elasticsearch [How does the Lucene Index work?](https://stackoverflow.com/questions/2602253/how-does-lucene-index-documents)

Scrapy is built with Twisted deferred (asynchronous, concurrent code) [Deferred](https://twisted.readthedocs.io/en/twisted-19.10.0/web/howto/web-in-60/asynchronous-deferred.html)

