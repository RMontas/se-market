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

def getHighestProfit6D(allPrices, numMrk, numRec):
    highestProfit6Didx = np.array((0,0,0,0,0,0))
    highestProfit = 0.0

    for m0 in range(numMrk):
        for m1 in range(numMrk):
            for m2 in range(numMrk):
                for r0 in range(numRec):
                    for r1 in range(numRec):
                        for r2 in range(numRec):
                            if allPrices[m0,m1,m2,r0,r1,r2] > highestProfit:
                                highestProfit = allPrices[m0,m1,m2,r0,r1,r2]
                                highestProfit6Didx = [m0,m1,m2,r0,r1,r2]

    return highestProfit6Didx

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

def twoRoutes(rBuyCred, rSellCred, numMrk, numRec, topN):
    allPrices = np.arange(numMrk*numMrk*numMrk*numRec*numRec*numRec, dtype=np.float32)
    allPrices = np.reshape(allPrices, (numMrk,numMrk,numMrk,numRec,numRec,numRec))

    for m0 in range(numMrk):
        for m1 in range(numMrk):
            for m2 in range(numMrk):
                for r0 in range(numRec):
                    for r1 in range(numRec):
                        for r2 in range(numRec):
                            allPrices[m0,m1,m2,r0,r1,r2] = rBuyCred[m0,r0]/rSellCred[m0,r1]*rBuyCred[m1,r1]/rSellCred[m1,r2]*rBuyCred[m2,r2]/rSellCred[m2,r0] 
    
    topNProfitIdx = np.zeros((topN, 6), dtype=np.uint16)
    topNProfit = np.zeros((topN, 1))

    for n in range(topN):
        highestProfit6Didx = getHighestProfit6D(allPrices, numMrk, numRec)
        topNProfitIdx[n,0] = highestProfit6Didx[0]
        topNProfitIdx[n,1] = highestProfit6Didx[1]
        topNProfitIdx[n,2] = highestProfit6Didx[2]
        topNProfitIdx[n,3] = highestProfit6Didx[3]
        topNProfitIdx[n,4] = highestProfit6Didx[4]
        topNProfitIdx[n,5] = highestProfit6Didx[5]
        topNProfit[n] = allPrices[topNProfitIdx[n,0], topNProfitIdx[n,1], topNProfitIdx[n,2], topNProfitIdx[n,3], topNProfitIdx[n,4], topNProfitIdx[n,5]]
        allPrices[topNProfitIdx[n,0], topNProfitIdx[n,1], topNProfitIdx[n,2], topNProfitIdx[n,3], topNProfitIdx[n,4], topNProfitIdx[n,5]] = 0

    return topNProfit, topNProfitIdx

def threeRoutes(rBuyCred, rSellCred, numMrk, numRec, topN):
    pass

def processTopN1R(topNProfit, topNProfitIdx, mrk, rec, topN):
    
    #out = np.empty([topN, 1], dtype="S10")
    for n in range(0,topN,2):
        print(str("{:.2f}".format((topNProfit[n,0]-1)*100)) + "% - " + \
              str(mrk[topNProfitIdx[n,0]]) + \
        "(" + str(rec[topNProfitIdx[n,2]]) + "-" + str(rec[topNProfitIdx[n,3]]) + ") --- " + \
              str(mrk[topNProfitIdx[n,1]]) + \
        "(" + str(rec[topNProfitIdx[n,3]]) + "-" + str(rec[topNProfitIdx[n,2]]) + ")")

    #print(out)

def processTopN2R(topNProfit, topNProfitIdx, mrk, rec, topN):
    for n in range(0,topN,3):
        print(str("{:.2f}".format((topNProfit[n,0]-1)*100)) + "% - " + 
              str(mrk[topNProfitIdx[n,0]]) + 
        "(" + str(rec[topNProfitIdx[n,3]]) + "-" + str(rec[topNProfitIdx[n,4]]) + ") --- " + 
              str(mrk[topNProfitIdx[n,1]]) + 
        "(" + str(rec[topNProfitIdx[n,4]]) + "-" + str(rec[topNProfitIdx[n,5]]) + ") --- " +  
              str(mrk[topNProfitIdx[n,2]]) + 
        "(" + str(rec[topNProfitIdx[n,5]]) + "-" + str(rec[topNProfitIdx[n,3]]) + ")")

def processTopN3R(topNProfit, topNProfitIdx, mrk, rec, topN):
    pass

def main():
    mrk = np.array(("Merc","Terr","Mart","Jup"))
    rec = np.array(("M","D","H","Z","N"))
    numMrk = 4 # Merc, Terr, Mart, Jup
    numRec = 5 # M, D, H, Z, N
    topN = 20 
    marketInput = 'market.txt'
    rBuyCred, rSellCred = getMarketStats(marketInput, numMrk, numRec)
    # calculate cheapest place to buy each Rec
    # calculate cheapest where you get more Rec1 out of your Rec0
    # calculate most profit with 1 route
    topNProfit, topNProfitIdx = oneRoute(rBuyCred, rSellCred, numMrk, numRec, topN)
    print("1 ROUTE")
    processTopN1R(topNProfit, topNProfitIdx, mrk, rec, topN)
    # calculate most profit with 2 routes
    topNProfit, topNProfitIdx = twoRoutes(rBuyCred, rSellCred, numMrk, numRec, topN)
    print("2 ROUTES")
    processTopN2R(topNProfit, topNProfitIdx, mrk, rec, topN)
    # calculate most profit with 3 routes

if __name__ == "__main__":
    main()
