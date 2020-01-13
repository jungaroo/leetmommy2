from flask import request
from flask_api import FlaskAPI, status
from lib.crawler import scrape_cohort_lectures
from lib.search import IndexController
from lib.schema import validator, LeetMommyValidator, QueryValidator
from lib.config import CONFIG
from flask_cors import CORS
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/ping', methods=['GET'])
def ping():
    """Pings server awake"""
    return {'ping': True}, status.HTTP_200_OK


@app.route("/scrape", methods=['POST'])
@validator(LeetMommyValidator)
def notes_list():
    """Updates the index from scraping"""
    cohort = request.json.get('cohort', None)
    client = IndexController.get_instance()

    if not client.index_exists(cohort):
        client.create_index(cohort)

    data = scrape_cohort_lectures(cohort=cohort)
    client.bulk_insert(index_name=cohort, json_data=data)
    return {'data': data}, status.HTTP_200_OK


@app.route("/search", methods=['GET'])
@validator(QueryValidator)
def search():
    """Returns raw data from the search result
    :param query: Query word or words to search for
    :param cohort: Either 'r11', 'r12', 'r13' for others
    """
    query = request.args.get('query', None)
    cohort = request.args.get('cohort', None)

    client = IndexController.get_instance()
    data = client.search(index_name=cohort, search_query=query)

    return {'data': data}, status.HTTP_200_OK


@app.route("/autocomplete", methods=['GET'])
@validator(QueryValidator)
def autocompleter():
    """Returns closest header words matching the word
    :param query: Query word or words to search for
    :param cohort: Either 'r11', 'r12', 'r13' or one of the cohorts
    """
    query = request.args.get('query', None)
    cohort = request.args.get('cohort', None)

    client = IndexController.get_instance()
    data = client.autocomplete(index_name=cohort, query_text=query)

    return {'data': data}, status.HTTP_200_OK


if __name__ == "__main__":
    app.run(debug=CONFIG.DEBUG)
