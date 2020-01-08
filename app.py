from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from lib.crawler import scrape_cohort_lectures
from lib.config import Config
from lib.search import IndexController

app = FlaskAPI(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """
    Pings server awake
    """
    return { 'ping': True }, status.HTTP_200_OK

@app.route("/scrape", methods=['GET'])
def notes_list():
    """
    Scrapes the lecture page for a cohort and creates and/or updates the Elastic Search Index
    @queryparam {cohort} Either 'r11', 'r12', 'r13' ... one of the Config.COHORTS
    """
    cohort = request.args.get('cohort', None)

    # TODO: https://pypi.org/project/flask-jsonschema-validator/
    if cohort not in Config.COHORTS:
        if cohort is None:
            error_message = 'Please provide ?cohort= query parameter.'
        else:
            error_message = f'{cohort} is not one of {Config.COHORTS}'

        return { 'error': error_message }, status.HTTP_400_BAD_REQUEST

    client = IndexController.get_instance()

    if not client.index_exists(cohort):
        client.create_index(cohort)
        
    data = scrape_cohort_lectures(cohort=cohort)
    client.bulk_insert(index_name=cohort, json_data=data)
    
    return { 'data': data }, status.HTTP_200_OK 

@app.route("/search", methods=['GET'])
def search():
    """
    Returns raw data from the search result
    @queryparam {query} Query word or words to search for
    @queryparam {cohort} Either 'r11', 'r12', 'r13' ... one of the Config.COHORTS
    """
    
    query = request.args.get('query', None)
    cohort = request.args.get('cohort', None)

    if cohort not in Config.COHORTS:
        if cohort is None:
            error_message = 'Please provide ?cohort= query parameter.'
        else:
            error_message = f'{cohort} is not one of {Config.COHORTS}'

        return { 'error': error_message }, status.HTTP_400_BAD_REQUEST

    if query is None:
        return { 'error': "Missing 'query' keyword query param"}, status.HTTP_400_BAD_REQUEST
        
    client = IndexController.get_instance()
    data = client.search(index_name=cohort, search_query=query)

    return { 'data': data }, status.HTTP_200_OK

@app.route("/autocomplete", methods=['GET'])
def autocompleter():
    """
    Returns closest header words matching the word 
    @queryparam {query} Query word or words to search for
    @queryparam {cohort} Either 'r11', 'r12', 'r13' ... one of the Config.COHORTS
    """
    
    query = request.args.get('query', None)
    cohort = request.args.get('cohort', None)

    if cohort not in Config.COHORTS:
        if cohort is None:
            error_message = 'Please provide ?cohort= query parameter.'
        else:
            error_message = f'{cohort} is not one of {Config.COHORTS}'

        return { 'error': error_message }, status.HTTP_400_BAD_REQUEST

    if query is None:
        return { 'error': "Missing 'query' keyword query param"}, status.HTTP_400_BAD_REQUEST
        
    client = IndexController.get_instance()
    data = client.autocomplete(index_name=cohort, query_text=query)

    return { 'data': data }, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(debug=True)