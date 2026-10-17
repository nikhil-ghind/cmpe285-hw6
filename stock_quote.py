import json
import urllib.request
from datetime import datetime

URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}"


def get_quote(symbol):
    request = urllib.request.Request(URL.format(symbol), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=10) as response:
        meta = json.load(response)["chart"]["result"][0]["meta"]
    price = meta["regularMarketPrice"]
    change = price - meta["chartPreviousClose"]
    percent = change / meta["chartPreviousClose"] * 100
    return meta.get("longName") or meta["shortName"], price, change, percent


def main():
    while True:
        symbol = input("Please enter a symbol:\n").strip().upper()
        if not symbol:
            break
        try:
            name, price, change, percent = get_quote(symbol)
            print(datetime.now().astimezone().strftime("%a %b %d %H:%M:%S %Z %Y"))
            print(f"{name} ({symbol})")
            print(f"{price:.2f} {change:+.2f} ({percent:+.2f}%)\n")
        except Exception:
            print("Error: invalid symbol or no network connection\n")


if __name__ == "__main__":
    main()
