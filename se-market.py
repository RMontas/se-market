import numpy as np
import re
import math
import heapq

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

def getHighestProfit4D(allPrices, numMrk, numRec):

    highestProfit4Didx = np.array((0,0,0,0))
    highestProfit = 0.0

    for m0 in range(numMrk):
        for m1 in range(numMrk):
            for r0 in range(numRec):
                for r1 in range(numRec):
                    if allPrices[m0,m1,r0,r1] > highestProfit:
                        highestProfit = allPrices[m0,m1,r0,r1]
                        highestProfit4Didx = [m0,m1,r0,r1]

    return highestProfit4Didx

def oneRoute(rBuyCred, rSellCred, numMrk, numRec, topN):

    allPrices = np.arange(numMrk*numMrk*numRec*numRec, dtype=np.float32)
    allPrices = np.reshape(allPrices, (numMrk,numMrk,numRec,numRec))

    for m0 in range(numMrk):
        for m1 in range(numMrk):
            for r0 in range(numRec):
                for r1 in range(numRec):
                    allPrices[m0,m1,r0,r1] = rBuyCred[m0,r0]/rSellCred[m0,r1]*rBuyCred[m1,r1]/rSellCred[m1,r0] 
    
    topNProfitIdx = np.zeros((topN, 4), dtype=np.uint16)
    topNProfit = np.zeros((topN, 1))

    for n in range(topN):
        highestProfit4Didx = getHighestProfit4D(allPrices, numMrk, numRec)
        topNProfitIdx[n,0] = highestProfit4Didx[0]
        topNProfitIdx[n,1] = highestProfit4Didx[1]
        topNProfitIdx[n,2] = highestProfit4Didx[2]
        topNProfitIdx[n,3] = highestProfit4Didx[3]
        topNProfit[n] = allPrices[topNProfitIdx[n,0], topNProfitIdx[n,1], topNProfitIdx[n,2], topNProfitIdx[n,3]]
        allPrices[topNProfitIdx[n,0], topNProfitIdx[n,1], topNProfitIdx[n,2], topNProfitIdx[n,3]] = 0

    return topNProfit, topNProfitIdx

def main():
    mrk = np.array(("Merc","Terr","Mart","Jup"))
    rec = np.array(("M","D","H","Z","N"))
    numMrk = 4 # Merc, Terr, Mart, Jup
    numRec = 5 # M, D, H, Z, N
    topN = 20
    marketInput = 'market.txt'
    rBuyCred, rSellCred = getMarketStats(marketInput, numMrk, numRec)
    # calculate most profit with 1 route
    topNProfit, topNProfitIdx = oneRoute(rBuyCred, rSellCred, numMrk, numRec, topN)

    print(topNProfit)
    print(topNProfitIdx)

if __name__ == "__main__":
    main()
