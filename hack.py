import websocket
import threading
import time
import argparse
import json
from flask import Flask, request

list = []

def on_message(ws, message):
    print(message)
    entry = json.loads(message)
    list.append(entry)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run():
        ws.send("")
        time.sleep(1)
        ws.close()
    threading.Thread(target=run).start()

# Default Flask site
app = Flask(__name__)
@app.route("/")
def hello():
    return "Try Querying!"

# Try querying at http://52.175.234.174:5000/stock with tickers, start, and end as parameters
@app.route("/stock", methods=['GET'])
def urlQuery():
    list.clear()
    symbols = request.args.get('tickers')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    symbols = symbols.split(',')

    websocket.enableTrace(True)

    stockPrices(symbols, start_date, end_date)

def stockPrices(symbols, start, end):
    websocket.enableTrace(True)

    for symbol in symbols:
        url = 'ws://34.214.11.52/stream?symbol={}&start={}&end={}'.format(symbol, start, end)

        ws = websocket.WebSocketApp(url,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()

# Main function if you want to run from terminal
def main():
    parser = argparse.ArgumentParser(description='gettin some market data')
    parser.add_argument('--start_date', required=True, help="Enter a valid start date in YYYYMMDD format")
    parser.add_argument('--end_date', required=True, help="Enter a valid end date in YYYYMMDD format")
    parser.add_argument('--symbols', required=True, help="Enter a ticker symbol or list of tickers. E.g. NDAQ or NDAQ,AAPL,MSFT")

    args = parser.parse_args()

    symbols = args.symbols.split(',')

    stockPrices(symbols. args.start_date, args.end_date)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
