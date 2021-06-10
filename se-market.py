
def getMarketStats(mrk):
    with open(mrk) as f:
        mrkIn = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    mrkIn = [x.strip() for x in mrkIn]
    mrkInClean = list() 
    mrkInClean.append(mrkIn[2])
    mrkInClean.append(mrkIn[3])
    mrkInClean.append(mrkIn[5])
    mrkInClean.append(mrkIn[6])
    mrkInClean.append(mrkIn[8])
    mrkInClean.append(mrkIn[9])
    mrkInClean.append(mrkIn[11])
    mrkInClean.append(mrkIn[12])
    print(mrkInClean)



def main():
    marketInput = 'market.txt'
    getMarketStats(marketInput)

if __name__ == "__main__":
    main()
