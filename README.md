# Leetmommy 2.0

Leetmommy is an open source search engine JSON API backed by ElasticSearch (7.5.1) and scrapy for Rithm school lectures.

Deployed:
{url here}

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
Run bin/elasticsearch or (bin\elasticsearch.bat) on Windows.  port 9200
Run bin/kibana or (bin\kibana.bat) on Windows. on port 5601

Type:
```
flask run
```

Open on localhost:5000

# Tests

```
python3 -m unittest
```
todo
