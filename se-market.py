import numpy as np
import re
import math

def getMarketStats(mrk, numMrk, numRec):
    with open(mrk) as f:
        mrkIn = f.readlines()
    mrkIn = [x.strip() for x in mrkIn]
    mrkInClean = []
    mrkInClean.append(mrkIn[2])
    mrkInClean.append(mrkIn[3])
    mrkInClean.append(mrkIn[5])
    mrkInClean.append(mrkIn[6])
    mrkInClean.append(mrkIn[8])
    mrkInClean.append(mrkIn[9])
    mrkInClean.append(mrkIn[11])
    mrkInClean.append(mrkIn[12])
    mrkRatiosBuyCred = np.zeros((numMrk, numRec))
    mrkRatiosSellCred = np.zeros((numMrk, numRec))
    for l in range(0,len(mrkInClean),2):
        A = re.split(r'\t+', mrkInClean[l].rstrip('\t'))
        A = [item.replace('.','') for item in A]
        A = [item.replace(',','.') for item in A]
        mrkRatiosBuyCred[math.floor(l/2),:] = np.array(A, dtype=np.float32)
    for l in range(1,len(mrkInClean),2):
        A = re.split(r'\t+', mrkInClean[l].rstrip('\t'))
        A = [item.replace('.','') for item in A]
        A = [item.replace(',','.') for item in A]
        mrkRatiosSellCred[math.floor(l/2),:] = np.array(A, dtype=np.float32)

    return mrkRatiosBuyCred, mrkRatiosSellCred

def main():
    numMrk = 4
    numRec = 5
    marketInput = 'market.txt'
    rBuyCred, rSellCred = getMarketStats(marketInput, numMrk, numRec)

    print(rBuyCred)
    print(rSellCred)


if __name__ == "__main__":
    main()
