# Leetmommy 2.0

Leetmommy is open source.
JSON Flask API for a search engine backed by ElasticSearch (7.5.1) and scrapy for Rithm school lectures.

# API Documentation

todo

# Installation (for development)

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set environmental variable to DEVELOPMENT. 

Download Elasticsearch & Kibana:
(Works with version 7.5.1)
https://www.elastic.co/downloads/elasticsearch

(Works with version 7.5.1)
https://www.elastic.co/downloads/kibana

# Spin up for development:
Run bin/elasticsearch or (bin\elasticsearch.bat) on Windows on port 9200
Run bin/kibana or (bin\kibana.bat) on Windows on port 5601

Type:
```
flask run
```

Open on localhost:5000

# Tests

todo
