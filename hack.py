import sys
import websocket
import threading
import time
import requests
import argparse
from pprint import pprint
import json

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

def main():
    parser = argparse.ArgumentParser(description='gettin some market data')
    parser.add_argument('--start_date', required=True, help="Enter a valid start date in YYYYMMDD format")
    parser.add_argument('--end_date', required=True, help="Enter a valid end date in YYYYMMDD format")
    parser.add_argument('--symbols', required=True, help="Enter a ticker symbol or list of tickers. E.g. NDAQ or NDAQ,AAPL,MSFT")

    args = parser.parse_args()

    websocket.enableTrace(True)

    symbols = args.symbols.split(',')

    for symbol in symbols:
        url = 'ws://34.214.11.52/stream?symbol={}&start={}&end={}'.format(symbol,args.start_date,args.end_date)
 
        ws = websocket.WebSocketApp(url,
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()
        with open('AAPLprices.json', 'w', newline='') as stockPrices:
            print(list)
            stockPrices.write(json.dumps(list))

if __name__ == "__main__":
   main() 
