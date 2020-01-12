from elasticsearch import Elasticsearch, client
from elasticsearch.helpers import bulk
from lib.config import CONFIG

DEFAULT_BODY = {
    "settings": {
        # We use the hobby tier, keep these values at minimum.
        "number_of_shards": 1,
        "number_of_replicas": 0,

        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 8,
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
    """Controller class for managing the Indices """

    _instance = None

    @classmethod
    def get_instance(cls):
        """Gets the singleton instance """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Private constructor for initializing the singleton instance.
        `This should not be invoked. Call IndexController.get_instance()`
        """
        if IndexController._instance:
            raise Exception('Singleton class - cannot reconstruct')
        else:
            self.es = Elasticsearch(CONFIG.ELASTIC_SEARCH_URL)
            self.cli = client.IndicesClient(self.es)

    def create_index(self, index_name: str, body=DEFAULT_BODY):
        """Creates an elastic search index
        :param index_name: name of the index
        :param body: ElasticSearch settings with mappings
        """
        if self.index_exists(index_name):
            self.delete_index(index_name)

        return self.cli.create(index=index_name, body=body)

    def delete_index(self, index_name: str):
        """Deletes an index
        :param index_name: name of the index
        """
        return self.cli.delete(index=index_name)

    def index_exists(self, index_name: str):
        return self.es.indices.exists(index=index_name)

    def bulk_insert(self, index_name: str, json_data):
        """Performs a bulk insert from a json_data array produced from scrapy
        :param index_name: name of the index
        """
        documents = IndexController.parse_pages(
            json_data=json_data, index_name=index_name)

        bulk(self.es, documents, index=index_name)
        self.refresh(index_name=index_name)

    def document_exists(self, index_name: str, _id: str):
        """Checks if a document exists in the index by id
        :param index_name: name of the index
        :param _id: identifier for the document
        """
        return self.es.exists(index_name, id=_id)

    def refresh(self, index_name: str):
        """Refreshes indices so newly added docs can be indexed and searched
        :param index_name: name of the index
        """
        self.es.indices.refresh(index=index_name)

    def autocomplete(self, index_name: str, query_text: str):
        """Returns suggested titles based on an n-grams
        :param index_name: Name of the index
        :param query_text: Partial word
        :return: List of documents whose titles match
        """
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
        """Searches index for documents using query
        :param index_name: Name of the index
        :param search_query: Search word or words
        :return: List of documents matching the search
        """
        body = {
            "query": {
                "multi_match": {
                    "query": search_query,
                    # Titles should have highest boost
                    "fields": [
                        "headers^1.1",
                        "bullets",
                        "text",
                        "title^1.25",
                        "code^0.8"
                    ],
                    "operator": "and",
                    "fuzziness": "2",  # Levenshtein edit distance
                }
            }
        }

        results = self.es.search(index_name, body=body)

        return [r['_source'] for r in results['hits']['hits']]

    @staticmethod
    def parse_pages(json_data, index_name: str):
        """Converts data into document objects.
        :param json_data: List of document objects scraped.
        :yield: Document upsert objects
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

    cli = IndexController.get_instance()
    cli.delete_index('demo11')
    cli.create_index('demo11')
    import crawler

    data = crawler.scrape_cohort_lectures('r11')
    cli.bulk_insert(json_data=data, index_name='rithm11')

    res = cli.search(search_query='mongodb', index_name='rithm11')
    print("Results:", len(res), res)
    # res = cli.autocomplete('rithm11', 'rea')
