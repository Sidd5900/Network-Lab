import matplotlib.pyplot as plt
import queue as Q
import math
import random

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
    def __init__(self, srcID, bandSrcToSwitch):
        self.srcID = srcID
        self.bandSrcToSwitch = bandSrcToSwitch


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
        return -math.log(1.0 - random.uniform(0,1)) / rateParameter

# function to calculate avg delay
def calculateAvgQueueSize(sourceCount, bandSrcToSwitch, bandSwitchToSink, pktLength,simTime,rate):
    packet = []
    avgQueuingDelay = 0.0
    switchObject = SWITCH(bandSwitchToSink)

    # pq is priority queue on the basis of event current time
    pq = Q.PriorityQueue()

    # generating first packet from every source at t=0
    for i in range(sourceCount):
        packet.append(PACKET(i, 0, i))
        pq.put(EVENT(0, i, 0))

    totalPktGenCount = sourceCount
    lastDispatchStartTime = 0.0
    avgSize = 0
    iterationCount = 0

    simTime = 5000
    pktReachSinkCount = 0
    while (pktReachSinkCount < simTime):
        avgSize+=switchObject.qSize
        iterationCount+=1
        x = pq.get()
        pktID = x.pktID
        occurTime = x.occurTime

        if x.status == 0:
            nextTim = nextPktGenTime(rate)
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
            switchObject.qSize = switchObject.qSize + 1

        elif x.status == 2:
            switchObject.qSize = switchObject.qSize - 1
            lastDispatchStartTime = occurTime
            sTime = occurTime + pktLength / bandSwitchToSink
            packet[pktID].sinkReachTime = sTime
            pq.put(EVENT(3, pktID, sTime))
        else:
            pktReachSinkCount+=1

    return avgSize/iterationCount


def main():
    sourceCount = 4  # number of source

    bandSrcToSwitch = 2e6  # bandwidth between source and switch (bits/s)

    bandSwitchToSink = 5e6  # bandwidth between switch and sink (bits/s)

    pktLength = 1e4  # packet size in bits

    simTime = 1000  # simulation time

    # x and y holds value of lamda and queue Size
    x = []
    y = []

    # creating source object
    source = []
    for i in range(sourceCount):
        source.append(SOURCE(i, bandSrcToSwitch))

    lamda = 5
    iterationCount = 20

    while lamda < 1000:
        x.append(lamda)
        iter = 0
        qSize = 0
        while iter < iterationCount:
            qSize +=calculateAvgQueueSize(sourceCount,bandSrcToSwitch,bandSwitchToSink,pktLength,simTime,lamda/sourceCount)
            iter+=1
        print(lamda,qSize/iterationCount)
        y.append(qSize/iterationCount)
        lamda+=100

    plt.plot(x, y)
    plt.xlabel("lambda")
    plt.ylabel("Average Queue Size")
    plt.title("Average Queue Size vs lambda")
    plt.show()


if __name__ == "__main__":
    main()