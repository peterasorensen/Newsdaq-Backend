import aylien_news_api
from aylien_news_api.rest import ApiException
import argparse
import json
import datetime
from flask import Flask, request

app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World"

@app.route("/articles", methods=['GET'])
def main():
    symbols = request.args.get('tickers')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    # Configure API key authorization: app_id
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'ec47511b'
    # Configure API key authorization: app_key
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '1747cc0619cd33c1e202fa7064c1fa6b'

    # create an instance of the API class
    api_instance = aylien_news_api.DefaultApi()

    opts = {
        'title': symbols,
        'sort_by': 'relevance',
        'source_locations_country': ['US'],
        'entities_title_type': ['Company'],
        'language': ['en'],
        'not_language': ['es', 'it'],
        'published_at_start': start_date,
        'published_at_end': end_date,
    }

    try:
        # List stories
        api_response = api_instance.list_stories(**opts)
        print("API called successfully. Returned data: ")
        print("========================================")
        list = []
        for story in api_response.stories:
          entry = {'title': story.title,
                   'date': story.published_at,
                   'titlePolarity': story.sentiment.title.polarity,
                   'titlePolarityScore': story.sentiment.title.score,
                   'bodyPolarity': story.sentiment.body.polarity,
                   'bodyPolarityScore': story.sentiment.body.score,
                   'URL': story.links.permalink}
          list.append(entry)
        print(json.dumps(list, default=myconverter))
        return json.dumps(list, default=myconverter)
          # print(story.title + " / " + story.source.name)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()[:11]

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)