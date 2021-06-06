import codecs

def getMarketStats(html):
    f=codecs.open(html, 'r')
    return f.read()

def main():
    htmlMarket = 'market.html'
    marketStats=getMarketStats(htmlMarket)
    print(marketStats)

if __name__ == "__main__":
    main()