import matplotlib.pyplot as plt
import queue as Q
import math
import random

# class for packet
class PACKET:
    def __init__(self, pktID, generateTime, srcID):
        self.pktID = pktID
        self.srcID = srcID
        self.generateTime = generateTime
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
# Status0 = packet is generated and ready to transfer to the switch via the link
# Status1 = packet reaches the queue
# Status2 = packet is ready to dispatch from the queue
# Status3 = packet reached the sink
class EVENT:
    def __init__(self, status, pktID, time):
        self.status = status
        self.pktID = pktID
        self.occurTime = time

    def __lt__(self, other):
        return self.occurTime < other.occurTime

#Packet generation follows Poisson's distribution
#Calculating time taken to generate next packet = -(1/lambda)*ln(1-U) where U is random no. between 0 and 1
def nextPktGenTime(rateParameter):
    return -math.log(1.0 - random.uniform(0, 1)) / rateParameter


# function to calculate avg delay
def calculateAvgDelay(sourceCount, bandSrcToSwitch, bandSwitchToSink, pktLength, simTime, rate):
    packet = []
    avgDelay = 0.0
    switchObject = SWITCH(bandSwitchToSink)

    # pq is priority queue (min heap) based on occurrence time of the event
    pq = Q.PriorityQueue()

    # generating first packet from every source at t=0
    for i in range(sourceCount):
        packet.append(PACKET(i, 0, i))
        pq.put(EVENT(0, i, 0))

    pcount = 0
    totalPktGenCount = sourceCount
    lastDispatchStartTime = 0.0


    simTime = 1000
    occurTime = 0
    pktReachSinkCount = 0

    while (pktReachSinkCount < simTime):
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
            #queue delay due to packets in the queue
            rtime = (switchObject.qSize * pktLength) / bandSwitchToSink
            #queue delay due to packet currently being dispatched
            tx = 0
            if packet[pktID].qReachTime - lastDispatchStartTime < (pktLength / bandSwitchToSink):
                tx = max(0, (pktLength / bandSwitchToSink) - (packet[pktID].qReachTime - lastDispatchStartTime))
            if lastDispatchStartTime == 0:
                tx = 0
            pq.put(EVENT(2, pktID, occurTime + rtime + tx))
            packet[pktID].qDispatchTime = occurTime + rtime + tx
            avgDelay = avgDelay + packet[pktID].qDispatchTime - packet[pktID].generateTime + pktLength / bandSwitchToSink
            switchObject.qSize = switchObject.qSize + 1
            pcount = pcount + 1

        elif x.status == 2:
            switchObject.qSize = switchObject.qSize - 1
            lastDispatchStartTime = occurTime
            sTime = occurTime + pktLength / bandSwitchToSink
            packet[pktID].sinkReachTime = sTime
            pq.put(EVENT(3, pktID, sTime))
        else:
            pktReachSinkCount += 1

    avgDelay = avgDelay / pcount

    return avgDelay


def main():

    sourceCount = 4             #number of source

    bandSrcToSwitch = 2e6       #bandwidth between source and switch (bits/s)

    bandSwitchToSink = 5e6    #bandwidth between switch and sink (bits/s)

    pktLength = 1e4           #packet size in bits

    simTime = 1000              #simulation time

    lambdaList = []
    avgDelayList = []

    # creating source object
    source = []
    for i in range(sourceCount):
        source.append(SOURCE(i, bandSrcToSwitch))

    lamda = 5
    iterationCount = 20
    while lamda < 1000:
        lambdaList.append(lamda)
        iter = 0
        delay = 0
        while iter < iterationCount:
            delay += calculateAvgDelay(sourceCount, bandSrcToSwitch, bandSwitchToSink, pktLength, simTime, lamda / sourceCount)
            iter += 1
        print(lamda, delay / iterationCount)
        avgDelayList.append(delay / iterationCount)
        lamda += 50

    plt.plot(lambdaList, avgDelayList)
    plt.xlabel("lambda")
    plt.ylabel("Average Delay")
    plt.title("Average delay vs lambda")
    plt.show()


if __name__ == "__main__":
    main()
