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

def getHighestProfit8D(allPrices, numMrk, numRec):
    highestProfit8Didx = np.array((0,0,0,0,0,0))
    highestProfit = 0.0

    for m0 in range(numMrk):
        for m1 in range(numMrk):
            for m2 in range(numMrk):
                for m3 in range(numMrk):
                    for r0 in range(numRec):
                        for r1 in range(numRec):
                            for r2 in range(numRec):
                                for r3 in range(numRec):
                                    if allPrices[m0,m1,m2,m3,r0,r1,r2,r3] > highestProfit:
                                        highestProfit = allPrices[m0,m1,m2,m3,r0,r1,r2,r3]
                                        highestProfit8Didx = [m0,m1,m2,m3,r0,r1,r2,r3]

    return highestProfit8Didx

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
    allPrices = np.arange(numMrk*numMrk*numMrk*numMrk*numRec*numRec*numRec*numRec, dtype=np.float32)
    allPrices = np.reshape(allPrices, (numMrk,numMrk,numMrk,numMrk,numRec,numRec,numRec,numRec))

    for m0 in range(numMrk):
        for m1 in range(numMrk):
            for m2 in range(numMrk):
                for m3 in range(numMrk):
                    for r0 in range(numRec):
                        for r1 in range(numRec):
                            for r2 in range(numRec):
                                for r3 in range(numRec):
                                    allPrices[m0,m1,m2,m3,r0,r1,r2,r3] = rBuyCred[m0,r0]/rSellCred[m0,r1]*rBuyCred[m1,r1]/rSellCred[m1,r2]*rBuyCred[m2,r2]/rSellCred[m2,r3]*rBuyCred[m3,r3]/rSellCred[m3,r0] 
    
    topNProfitIdx = np.zeros((topN, 8), dtype=np.uint16)
    topNProfit = np.zeros((topN, 1))

    for n in range(topN):
        highestProfit8Didx = getHighestProfit8D(allPrices, numMrk, numRec)
        topNProfitIdx[n,0] = highestProfit8Didx[0]
        topNProfitIdx[n,1] = highestProfit8Didx[1]
        topNProfitIdx[n,2] = highestProfit8Didx[2]
        topNProfitIdx[n,3] = highestProfit8Didx[3]
        topNProfitIdx[n,4] = highestProfit8Didx[4]
        topNProfitIdx[n,5] = highestProfit8Didx[5]
        topNProfitIdx[n,6] = highestProfit8Didx[6]
        topNProfitIdx[n,7] = highestProfit8Didx[7]
        topNProfit[n] = allPrices[topNProfitIdx[n,0], topNProfitIdx[n,1], topNProfitIdx[n,2], topNProfitIdx[n,3], topNProfitIdx[n,4], topNProfitIdx[n,5], topNProfitIdx[n,6], topNProfitIdx[n,7]]
        allPrices[topNProfitIdx[n,0], topNProfitIdx[n,1], topNProfitIdx[n,2], topNProfitIdx[n,3], topNProfitIdx[n,4], topNProfitIdx[n,5], topNProfitIdx[n,6], topNProfitIdx[n,7]] = 0

    return topNProfit, topNProfitIdx

def processTopN1R(topNProfit, topNProfitIdx, mrk, rec, topN):
    for n in range(0,topN,2):
        print(str("{:.2f}".format((topNProfit[n,0]-1)*100)) + "% - " + \
              str(mrk[topNProfitIdx[n,0]]) + \
        "(" + str(rec[topNProfitIdx[n,2]]) + "-" + str(rec[topNProfitIdx[n,3]]) + ") --- " + \
              str(mrk[topNProfitIdx[n,1]]) + \
        "(" + str(rec[topNProfitIdx[n,3]]) + "-" + str(rec[topNProfitIdx[n,2]]) + ")")

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
    for n in range(0,topN,4):
        print(str("{:.2f}".format((topNProfit[n,0]-1)*100)) + "% - " + 
              str(mrk[topNProfitIdx[n,0]]) + 
        "(" + str(rec[topNProfitIdx[n,4]]) + "-" + str(rec[topNProfitIdx[n,5]]) + ") --- " + 
              str(mrk[topNProfitIdx[n,1]]) + 
        "(" + str(rec[topNProfitIdx[n,5]]) + "-" + str(rec[topNProfitIdx[n,6]]) + ") --- " +  
              str(mrk[topNProfitIdx[n,2]]) + 
        "(" + str(rec[topNProfitIdx[n,6]]) + "-" + str(rec[topNProfitIdx[n,7]]) + ") --- " +
              str(mrk[topNProfitIdx[n,3]]) + 
        "(" + str(rec[topNProfitIdx[n,7]]) + "-" + str(rec[topNProfitIdx[n,4]]) + ")")

def cheapestMarktPerRec(rSellCred, numMrk, numRec):
    cheapestM = np.zeros((numRec, 1), dtype=np.uint16)
    for r in range(numRec):
        cheapestR = 100000
        for m in range(numMrk):
            if rSellCred[m,r] < cheapestR:
                cheapestR = rSellCred[m,r]
                cheapestM[r] = m

    return cheapestM

def processCheapestMarktPerRec(cheapestR, mrk, rec, rSellCred):
    for r in range(rec.shape[0]):
        print("Cheapest " + str(rec[r]) + " -- " + str(mrk[cheapestR[r]]) + "(" + str(rSellCred[cheapestR[r],r]) + ")")

def calcBestMarkt(r0, r1, allPrices, numMrk):
    bestM = 0
    bestR1 = 0

    for m in range(numMrk): 
        if allPrices[r0, r1, m] > bestR1:
            bestR1 = np.ceil(allPrices[r0, r1, m])
            bestM = m

    return bestM, bestR1

def calcCheapestMarktForGivenTrade(rBuyCred, rSellCred, numMrk, numRec):

    allPrices = np.arange(numMrk*numRec*numRec, dtype=np.float32)
    allPrices = np.reshape(allPrices, (numRec,numRec,numMrk))

    for r0 in range(numRec):
        for r1 in range(numRec):
            for m0 in range(numMrk):
                allPrices[r0,r1,m0] = 5000*rBuyCred[m0,r0]/rSellCred[m0,r1] 
    
    bestM0 = np.zeros((numRec, numRec), dtype=np.uint32)
    bestR1 = np.zeros((numRec, numRec), dtype=np.uint32)

    for r0 in range(numRec):
        for r1 in range(numRec):
            for m0 in range(numMrk):
                bestM0[r0, r1], bestR1[r0, r1] = calcBestMarkt(r0, r1, allPrices, numMrk)

    return bestM0, bestR1

def processMarktTables(bestM0, bestR1, mrk, rec):

    print("Best market for r0 (ver) for r1 (hor)")
    print("\t" + rec[0] + "\t" + rec[1] + "\t" + rec[2] + "\t" + rec[3] + "\t" + rec[4])
    print(rec[0] + "\t" + "---" + "\t" + mrk[bestM0[0,1]] + "\t" + mrk[bestM0[0,2]] + "\t" + mrk[bestM0[0,3]] + "\t" + mrk[bestM0[0,4]])
    print(rec[1] + "\t" + mrk[bestM0[1,0]] + "\t" + "---" + "\t" + mrk[bestM0[1,2]] + "\t" + mrk[bestM0[1,3]] + "\t" + mrk[bestM0[1,4]])
    print(rec[2] + "\t" + mrk[bestM0[2,0]] + "\t" + mrk[bestM0[2,1]] + "\t" + "---" + "\t" + mrk[bestM0[2,3]] + "\t" + mrk[bestM0[2,4]])
    print(rec[3] + "\t" + mrk[bestM0[3,0]] + "\t" + mrk[bestM0[3,1]] + "\t" + mrk[bestM0[3,2]] + "\t" + "---" + "\t" + mrk[bestM0[3,4]])
    print(rec[4] + "\t" + mrk[bestM0[4,0]] + "\t" + mrk[bestM0[4,1]] + "\t" + mrk[bestM0[4,2]] + "\t" + mrk[bestM0[4,3]] + "\t" + "---")

    print("Highest ammount of r1 from top table for 5000 of r0")
    print("\t" + rec[0] + "\t" + rec[1] + "\t" + rec[2] + "\t" + rec[3] + "\t" + rec[4])
    print(rec[0] + "\t" + "---" + "\t" + str(bestR1[0,1]) + "\t" + str(bestR1[0,2]) + "\t" + str(bestR1[0,3]) + "\t" + str(bestR1[0,4]))
    print(rec[1] + "\t" + str(bestR1[1,0]) + "\t" + "---" + "\t" + str(bestR1[1,2]) + "\t" + str(bestR1[1,3]) + "\t" + str(bestR1[1,4]))
    print(rec[2] + "\t" + str(bestR1[2,0]) + "\t" + str(bestR1[2,1]) + "\t" + "---" + "\t" + str(bestR1[2,3]) + "\t" + str(bestR1[2,4]))
    print(rec[3] + "\t" + str(bestR1[3,0]) + "\t" + str(bestR1[3,1]) + "\t" + str(bestR1[3,2]) + "\t" + "---" + "\t" + str(bestR1[3,4]))
    print(rec[4] + "\t" + str(bestR1[4,0]) + "\t" + str(bestR1[4,1]) + "\t" + str(bestR1[4,2]) + "\t" + str(bestR1[4,3]) + "\t" + "---")

def main():
    mrk = np.array(("Merc","Terr","Mart","Jup"))
    rec = np.array(("M","D","H","Z","N"))
    numMrk = 4 # Merc, Terr, Mart, Jup
    numRec = 5 # M, D, H, Z, N
    topN = 10 
    marketInput = 'market.txt'
    rBuyCred, rSellCred = getMarketStats(marketInput, numMrk, numRec)
    # calculate cheapest place to buy each Rec
    cheapestR = cheapestMarktPerRec(rSellCred, numMrk, numRec)
    processCheapestMarktPerRec(cheapestR, mrk, rec, rSellCred)
    # given r0 and r1 calculate cheapest market
    bestM0, bestR1 = calcCheapestMarktForGivenTrade(rBuyCred, rSellCred, numMrk, numRec)
    processMarktTables(bestM0, bestR1, mrk, rec)
    # calculate most profit with 1 route
    topNProfit, topNProfitIdx = oneRoute(rBuyCred, rSellCred, numMrk, numRec, topN)
    print("1 ROUTE")
    processTopN1R(topNProfit, topNProfitIdx, mrk, rec, topN)
    # calculate most profit with 2 routes
    topNProfit, topNProfitIdx = twoRoutes(rBuyCred, rSellCred, numMrk, numRec, topN)
    print("2 ROUTES")
    processTopN2R(topNProfit, topNProfitIdx, mrk, rec, topN)
    # calculate most profit with 3 routes
    topNProfit, topNProfitIdx = threeRoutes(rBuyCred, rSellCred, numMrk, numRec, topN)
    print("3 ROUTES")
    processTopN3R(topNProfit, topNProfitIdx, mrk, rec, topN)

if __name__ == "__main__":
    main()
