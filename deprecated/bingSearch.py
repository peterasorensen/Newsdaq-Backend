import json
import requests
import argparse
import csv

# def main():
#     parser = argparse.ArgumentParser(description='gettin some market data')
#     parser.add_argument('--start_date', required=True, help="Enter a valid start date in YYYYMMDD format")
#     parser.add_argument('--end_date', required=True, help="Enter a valid end date in YYYYMMDD format")
#     parser.add_argument('--symbols', required=True,
#                         help="Enter a ticker symbol or list of tickers. E.g. NDAQ or NDAQ,AAPL,MSFT")
#
#     args = parser.parse_args()


global_headers = {"Ocp-Apim-Subscription-Key": "3af8dba5b91c4f7b81b8536be7f3bac2"}
r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/search?q=AAPL&since=2016-10-07T01:01:01&sortBy=Date&offset=1000&count=100', headers=global_headers)
json1 = json.loads(r.text)
articleArr = json1["value"]



articlesList = []
for i in range(len(articleArr)):
    entry = {'name': articleArr[i]["name"],
             'description': articleArr[i]["description"],
             'url': articleArr[i]["url"],
             'date': articleArr[i]["datePublished"]}
    articlesList.append(entry)

print(articlesList)

with open('eggs.json', 'w', newline='') as jsonfile:
    jsonfile.write(json.dumps(articlesList))
    # for article in articlesList:
    #     spamwriter = csv.writer(csvfile)
    #     spamwriter.writerow([article["name"], article["description"], article["url"], article["datePublished"]])



# with open('AAPL.json', 'w') as f:
#     for article in articlesList:
#         a_dict = {'name': article[0], 'description': article[1], 'date': article[2]}
#         f.write(json.dumps(a_dict) + ", \n")
#     # json.dump(jsonArticles, f)

# for article in articlesList:
#     a_dict = {'name': article[0], 'description': article[1], 'date': article[2]}
#     with open('AAPL.json') as f:
#         data = json.load(f)
#     data.update(a_dict)
#     with open('AAPL.json', 'w') as f:
#         json.dump(data, f)