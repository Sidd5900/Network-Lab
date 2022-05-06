import matplotlib.pyplot as plt
import queue as Q
import math
import random

delayList = []

# class for packet
class PACKET:
    def __init__(self, pktID=0, gtime=0.0, srcID=0):
        self.pktID = pktID
        self.srcID = srcID
        self.generateTime = gtime
        self.qReachTime = -1
        self.qDispatchTime = -1
        self.sinkReachTime = -1


# class for source
class SOURCE:
    def __init__(self, srcID, bandSrcToSwitch, grate):
        self.srcID = srcID
        self.bandSrcToSwitch = bandSrcToSwitch
        self.rate = grate


# class for switch
class SWITCH:
    def __init__(self, bandwidth):
        self.bandSwitchToSink = bandwidth
        self.qSize = 0


# class for various Event
class EVENT:
    def __init__(self, status, pktID, t):
        self.status = status
        self.pktID = pktID
        self.occurTime = t

    def __lt__(self, other):
        return self.occurTime < other.occurTime


def nextPktGenTime(rateParameter):
    return -math.log(1.0 - random.uniform(0, 1)) / rateParameter


# function to calculate avg delay
def calculateAvgDelay(sourceCount, bandSrcToSwitch, bandSwitchToSink, pktLength, simTime, source):
    packet = []
    avgQueuingDelay = 0.0
    switchObject = SWITCH(bandSwitchToSink)

    # pq is priority queue on the basis of event current time
    pq = Q.PriorityQueue()

    # generating first packet from every source at t=0
    for i in range(sourceCount):
        packet.append(PACKET(i, 0, i))
        pq.put(EVENT(0, i, 0))

    avgDelay = []
    pSourceCount = []
    for i in range(len(source)):
        avgDelay.append(0)
        pSourceCount.append(0)
    pcount = 0
    totalPktGenCount = sourceCount
    lastDispatchStartTime = 0.0
    occurTime = 0
    pktReachSinkCount = 0
    simTime = 5000

    while (pktReachSinkCount < simTime):
        x = pq.get()
        pktID = x.pktID
        occurTime = x.occurTime
        srcID = packet[pktID].srcID

        if x.status == 0:
            nextTim = nextPktGenTime(source[srcID].rate)
            pq.put(EVENT(0, totalPktGenCount, occurTime + nextTim))
            packet.append(PACKET(totalPktGenCount, occurTime + nextTim, packet[pktID].srcID))
            totalPktGenCount = totalPktGenCount + 1
            pq.put(EVENT(1, pktID, occurTime + pktLength / bandSrcToSwitch))
            packet[pktID].qReachTime = occurTime + pktLength / bandSrcToSwitch

        elif x.status == 1:
            rtime = (switchObject.qSize * pktLength) / bandSwitchToSink
            tx = 0
            if packet[pktID].qReachTime - lastDispatchStartTime < (pktLength / bandSwitchToSink):
                tx = max(0, (pktLength / bandSwitchToSink) - (packet[pktID].qReachTime - lastDispatchStartTime))
            if lastDispatchStartTime == 0:
                tx = 0
            pq.put(EVENT(2, pktID, occurTime + rtime + tx))
            packet[pktID].qDispatchTime = occurTime + rtime + tx
            avgDelay[srcID] += packet[pktID].qDispatchTime - packet[pktID].generateTime + pktLength / bandSwitchToSink
            switchObject.qSize = switchObject.qSize + 1
            pSourceCount[srcID] += 1

        elif x.status == 2:
            switchObject.qSize = switchObject.qSize - 1
            lastDispatchStartTime = occurTime
            sTime = occurTime + pktLength / bandSwitchToSink
            packet[pktID].sinkReachTime = sTime
            pq.put(EVENT(3, pktID, sTime))
        else:
            pktReachSinkCount += 1

    for i in range(sourceCount):
        delayList[i].append(avgDelay[i] / pSourceCount[i])


def main():

    # sourceCount = number of source
    sourceCount = 4

    # bandSrcToSwitch = bandwidth between source and switch in bit
    bandSrcToSwitch = 4e5

    # bandSwitchToSink = bandwidth between switch and sink in bit
    bandSwitchToSink = 2e5
    # pktLength = size of each packet in bit
    pktLength = 1e4
    # gen rate for each source
    grate = [0.2, 1, 5, 15]
    # simulation time
    simTime = 1000


    # creating source object
    source = []
    for i in range(sourceCount):
        source.append(SOURCE(i, bandSrcToSwitch, grate[i]))
        delayList.append([])

    iter = 0
    while iter < 100:
        calculateAvgDelay(sourceCount, bandSrcToSwitch, bandSwitchToSink, pktLength, simTime, source)
        print(iter)
        iter += 1
    l = []
    for i in range(sourceCount):
        l.append("Source " + str(i))
    plt.title("Average Delay for each source")
    plt.ylabel("time unit")
    plt.xlabel("sources")
    plt.boxplot(delayList, labels=l)
    plt.show()


if __name__ == "__main__":
    main()