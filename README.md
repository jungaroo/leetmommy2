# Leetmommy 2.0

Leetmommy is an open source search engine JSON API backed by ElasticSearch (7.5.1) and scrapy for Rithm school lectures.

Here's a demo frontend app using the Leetmommy 2.0 API
[leetmommy.surge.sh](http://leetmommy.surge.sh)

# API Documentation

See `app.py` for the actual route source code.
## Resource URL (base URL)
```
http://leetmommy2.herokuapp.com/
```

| HTTP VERB | URL | Description |
| --- | ---| --- |
| GET | /ping | Just a dummy HTTP request to wake up the heroku servers. 
| GET | /search | Main searching to get list of documents 
| GET | /autocomplete | returns a list of documents that match the current word. 
---

## GET /ping
This route takes no parameters, it just wakes up the heroku server from sleeping.
Once finished, it will return a JSON object :
```
{ ping: true }
```

Sample usage 
```js
import axios from 'axios';
const BASE_URL = 'leetmommy2.herokuapp.com';

const wakeUpHeroku = async () => {
  const response = await axios.get(`${BASE_URL}/ping`);
}

wakeUpHeroku();
```

## GET /search?search={search}&cohort={cohort}
#### URI Parameters
| Name | Input | Required | Type | Description |
| --- | --- | --- | --- | --- |
| search | query | true | string | Space seperated string of search
| cohort | query | true | string | A cohort string. Either 'r11', 'r12', 'r13' or 'r14' etc. 

### Response
If successful parameters are passed: 

Returns a JSON, with property `data`:
Which is an array of rithm school lecture document objects.
Each document has these keys:

```json
{
  "title": "Python Tools & Techniques",
  "url": "http://curric.rithmschool.com/r13/lectures/python-tools/",
  "highlight": {
    "headers": [
      "<b>Python</b> Tools & Techniques"
    ],
    "code": [
        "$ <b>python3</b> -m doctest -v your-file.py",
        "$ cd my-project-directory $ <b>python3</b> -m venv venv"
    ],
    "text": [
        "In general, in <b>Python</b>: explicit is better than implicit",
        "<b>Python</b> includes dozens of useful libraries",
        "When using a new <b>Python</b> project:"
    ],
    "title": [
        "<b>Python</b> Tools & Techniques"
    ],
    "bullets": [
        "It makes certain <b>python</b> is the version of <b>Python</b> used",
        "You have access to the standard library of <b>Python</b>"
    ]
  }
}
```
Highlight keys are surrounded by <b>, and highlight where the match is found.
Headers, code, text, title, bullets are keys that tell where the text match was found.

Sample usage 
```js
import axios from 'axios';
const BASE_URL = 'leetmommy2.herokuapp.com';

const getLinks = async (words='Python', cohort='r13') => {
  const response = await axios.get(`${BASE_URL}/search?search=${words}&cohort=${cohort}`);
  const { documents } = response.data; 
  const links = documents.map((d) => d.url);
  return links;
}
```

## GET /search?search={search}&cohort={cohort}
#### URI Parameters
| Name | Input | Required | Type | Description |
| --- | --- | --- | --- | --- |
| search | query | true | string | Space seperated string of search
| cohort | query | true | string | A cohort string. Either 'r11', 'r12', 'r13' or 'r14' etc. 

### Response
If successful parameters are passed: 

Returns a JSON, with property `data`, a list of Lecture Note title suggestions.
```json
{
  "data": [
    "Python Wrap-Up",
    "Python Tools & Techniques",
    "Python Object Orientation",
    "Introduction to Python",
    "Python Data Structures"
  ]
}
```

```js
import axios from 'axios';
const BASE_URL = 'leetmommy2.herokuapp.com';

const getLinks = async (words='Python', cohort='r13') => {
  const response = await axios.get(`${BASE_URL}/autocomplete?search=${words}&cohort=${cohort}`);
  const { documents } = response.data; // Sorry for the double data key, maybe we should fix this
  return data;
}
```

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


# Nice to haves 

1) Allow custom surround for GET search/ route (right now defaults to <b> </b>)
2) Improve the fuzzy search configurations
3) Improve code snippet configurations. -> Tokenizing html correctly

# Extra reading

The old [leetmommy](https://github.com/odoland/leetmommy11) source code

Fuzzy matching - [Levenshtein Edit Distance](https://en.wikipedia.org/wiki/Levenshtein_distance)

Google's paper on [Anatomy of the Search Engine](http://infolab.stanford.edu/~backrub/google.html)

Elasticsearch [How does the Lucene Index work?](https://stackoverflow.com/questions/2602253/how-does-lucene-index-documents)

Scrapy is built with Twisted deferred (asynchronous, concurrent code) [Deferred](https://twisted.readthedocs.io/en/twisted-19.10.0/web/howto/web-in-60/asynchronous-deferred.html)

