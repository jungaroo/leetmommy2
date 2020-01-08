from datetime import datetime
from elasticsearch import Elasticsearch, client
from elasticsearch.helpers import bulk
import json
import base64

URL = 'http://localhost:9200'

DEFAULT_BODY = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 10,
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "autocomplete_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {"type": "text", "analyzer": "autocomplete"},
            "bullets": {"type": "text"},
            "headers": {"type": "text"},
            "text": {"type": "text"},
            "code": {"type": "text"},
            "url": {"type": "text"}
        }
    }
}


class IndexController:

    _instance = None

    @classmethod
    def get_instance(cls):
        """Gets the singleton instance """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Private constructor for initializing the singleton instance """
        if IndexController._instance:
            raise Exception('Singleton class - cannot reconstruct')
        else:
            self.es = Elasticsearch(URL)
            self.cli = client.IndicesClient(self.es)

    def create_index(self, index_name: str, body=DEFAULT_BODY):
        """Creates an index with the name. Provide the settings in the body according to the ElasticSearch Index API"""

        if self.index_exists(index_name):
            self.delete_index(index_name)

        return self.cli.create(index=index_name, body=body)

    def delete_index(self, index_name: str):
        """Deletes an index """
        return self.cli.delete(index=index_name)

    def index_exists(self, index_name: str):
        return self.es.indices.exists(index=index_name)

    def bulk_insert(self, index_name: str, json_data):
        """Performs a bulk insert from a json_data array produced from scrapy"""

        documents = IndexController.parse_pages(
            json_data=json_data, index_name=index_name)

        bulk(self.es, documents, index=index_name)
        
        self.refresh(index_name=index_name)

    def exists(index_name, _id):
        """ Checks if a document exists in the index by id """
        return self.es.exists(index_name, id=_id)

    def refresh(self, index_name: str):
        """Refreshes indices so newly added documents can be indexed and searched """
        self.es.indices.refresh(index=index_name)

    def autocomplete(self, index_name, query_text):
        """Returns an autocompleted list of titles """
        body = {
            "query": {
                "match": {
                    "title": {
                        "query": query_text,
                        "fuzziness": "0",
                        "analyzer": "standard",
                    }
                }
            }
        }
        results = self.es.search(index_name, body=body)
        return [r for r in results['hits']['hits']]

    def search(self, index_name: str, search_query: str):
        body = {
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": ["headers", "bullets", "text", "title", "code"],
                    "operator": "and",
                    "fuzziness": "3", # Levenshtein edit distance
                }
            }
        }

        results = self.es.search(index_name, body=body)

        return [r['_source'] for r in results['hits']['hits']]

    @staticmethod
    def parse_pages(json_data, index_name):
        """
        Goes through all the json data for the pages for the cohort and generates a document per page
        """

        for page in json_data:
            yield {
                "_id": page['url'],
                "_op_type": 'update',
                "doc_as_upsert": True,
                "doc": {
                    "title": page['title'],
                    "bullets": page['bullets'],
                    "headers": page['headers'],
                    "text": page['text'],
                    "code": page['code'],
                    "url": page['url'],
                }}


if __name__ == "__main__":
    # Sample usage:

    client = IndexController.get_instance()
    client.delete_index('rithm11')
    # client.create_index('rithm11')
    # import crawler

    # data = crawler.scrape_cohort_lectures('r11')
    # client.bulk_insert(json_data=data, index_name='rithm11')

    # res = client.search(search_query='react', index_name='rithm11')
    # print("Results:", len(res), res)
    # res = client.autocomplete('rithm11', 'rea')
