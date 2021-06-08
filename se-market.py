import codecs
import re

def makeTable(html):
    buyPattern = "<tr class=\"center mini blue b670\" height=\"22\">"          # recuros - cred
    sellPattern = "<tr class=\"center mini orange sep b670\" height=\"22\">"    # cred - recurso
    matches = re.finditer(buyPattern, html)
    matches_positions = [match.start() for match in matches]
    print(matches_positions)

def getMarketStats(html):
    f=codecs.open(html, 'r')
    return f.read()


def main():
    htmlMarket = 'market.html'
    marketStats=getMarketStats(htmlMarket)
    print(marketStats)
    makeTable(marketStats)

if __name__ == "__main__":
    main()