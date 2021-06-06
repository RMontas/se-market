import pandas as pd
import codecs

def makeTable(html):
    df = pd.read_html(html) # TRY BeautifulSoup
    print(df)

def getMarketStats(html):
    f=codecs.open(html, 'r')
    return f.read()

def main():
    htmlMarket = 'market.html'
    marketStats=getMarketStats(htmlMarket)
    print(marketStats)
    makeTable(htmlMarket)

if __name__ == "__main__":
    main()