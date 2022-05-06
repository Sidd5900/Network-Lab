import matplotlib.pyplot as plt
import queue as Q

utilNum = 0

#pktDrop = 0


# class for pcket
class DATAPACKET:
    def __init__(self, pktID=0, gtime=0.0, srcID=0):
        self.pktID = pktID
        self.srcID = srcID
        self.generateTime = gtime
        self.qReachTime = -1
        self.qDispatchTime = -1
        self.sinkReachTime = -1


# class for source
class DATASOURCE:
    def __init__(self, lamda, sid, bandSrcToSwitch):
        self.genRate = lamda
        self.srcID = sid
        self.bandSrcToSwitch = bandSrcToSwitch


# class for switch
class DATASWITCH:
    def __init__(self, bwidth):
        self.bandSwitchToSink = bwidth
        self.qSize = 0


# class for various Event
class EVENT:
    def __init__(self, status, pktID, t):
        self.status = status
        self.pktID = pktID
        self.occurTime = t

    def __lt__(self, other):
        return self.occurTime < other.occurTime


# function to calculate pktLossRate
def calculateAvgDelay(nSource, bandSrcToSwitch, bandSwitchToSink, pktLength, source, simTime):
    packet = []
    avgDelay = 0.0
    avgQueuingDelay = 0.0
    switchObject = DATASWITCH(bandSwitchToSink)
    #global pktDrop
    pktDrop = 0
    # pq is priority queue on the basis of event current time
    pq = Q.PriorityQueue()

    # generating first packet from every source at t=0
    for i in range(nSource):
        packet.append(DATAPACKET(i, 0, i))
        pq.put(EVENT(0, i, 0))

    pktCount = 0
    packetReachSink = 0
    pktTot = nSource
    lastLeftTime = 0
    packetarrived = 0
    # Simulating for fixed time
    # Event0 = generation of packet
    # Event1 = reaching Queue time
    # Event2 = leaving queue time
    # Event3 = reaching sink time
    occurTime = 0

    while (packetReachSink < simTime):
        x = pq.get()
        pktID = x.pktID
        occurTime = x.occurTime
        transDelaySrc = pktLength / bandSrcToSwitch
        transDelaySwitch = pktLength / bandSwitchToSink

        # Event 0 -> (Event0,Event1)
        if x.status == 0:
            rate = source[packet[pktID].srcID].genRate
            #generate next packet from the source of the current packet
            pq.put(EVENT(0, pktTot, occurTime + 1 / rate))
            packet.append(DATAPACKET(pktTot, occurTime + 1 / rate, packet[pktID].srcID))
            pktTot = pktTot + 1

            pq.put(EVENT(1, pktID, occurTime + transDelaySrc))
            packet[pktID].qReachTime = occurTime + transDelaySrc
        # Event 1 -> Event2,and if queue is full packet drop
        elif x.status == 1:
            #queuing delay
            qDelay = (switchObject.qSize * pktLength) / bandSwitchToSink

            #delay due to the last packet currently being dispatched
            if ((lastLeftTime != 0) and (occurTime < lastLeftTime + transDelaySwitch)):
                qDelay += transDelaySwitch - (occurTime - lastLeftTime)

            pq.put(EVENT(2, pktID, occurTime + qDelay))
            packet[pktID].qDispatchTime = occurTime + qDelay
            switchObject.qSize = switchObject.qSize + 1
            packet[pktID].sinkReachTime = occurTime + qDelay + transDelaySwitch
            # avgDelay += packet[pktID].sinkReachTime - packet[pktID].generateTime
            avgQueuingDelay += qDelay
            # pktCount = pktCount + 1
            avgDelay = avgDelay + packet[pktID].sinkReachTime - packet[pktID].generateTime
            pktCount = pktCount + 1

        # Event2 -> Event3
        elif x.status == 2:
            switchObject.qSize = switchObject.qSize - 1
            lastLeftTime = occurTime
            sinkReachTime = occurTime + transDelaySwitch
            pq.put(EVENT(3, pktID, sinkReachTime))
        #reached the sink
        else:
            packetReachSink+=1


    #return average delay
    print(avgDelay," ",pktCount)
    avgDelay = avgDelay / pktCount
    return avgDelay

    # return pktDroprate
    #return pktDrop / packetarrived



def main():
    print("Enter 0 to use default value or 1 to use own")
    resp = int(input())
    if resp == 0:
        # nsource = number of source
        nSource = 4

        # bs = bandwidth between source and switch in bit
        bandSrcToSwitch= 2e6

        # bss = bandwidth between switch and sink in bit
        bandSwitchToSinkhigh = 8e6
        bandSwitchToSinklow = 25e3
        # pktLength = size of each packet in bit
        pktLength = 1.2e4

        # grate = packet genrate
        grate = 16

        # simulation time
        simTime = 5000

    else:
        nSource = int(input("Enter Number of Source :"))
        bandSrcToSwitch = float(input("Enter bandwdth between Source and switch(bandSrcToSwitch) in bit:"))
        bandSwitchToSinklow = float(input("Enter bandwidth(lower bound) between switch and sink(bandSwitchToSink) in bit:"))
        bandSwitchToSinkhigh = float(input("Enter bandwidth(upper bound) between switch and sink(bandSwitchToSink) in bit:"))
        pktLength = int(input("Enter packet length in bit(pktlength) :"))
        grate = int(input("Enter packet generation rate:"))
        #if pktLength * grate >= bandSrcToSwitch:
        #    print("pktLength*grater should be less than bandSrcToSwitch")
        #    return 0
        simTime = int(input("Enter Simulation time:"))

    # utilNum = numerator of utilization factor i.e arrival rate
    global utilNum
    # x and y holds value of delay and utilizationfactor
    x = []
    y = []
    source = []
    for i in range(nSource):
        source.append(DATASOURCE(grate, i, bandSrcToSwitch))
        utilNum = utilNum + grate
    # varying curBandSwitchToSink i.e bandSwitchToSink for plotting
    curBandSwitchToSink = bandSwitchToSinklow
    while (curBandSwitchToSink < bandSwitchToSinkhigh):
        Ufactor = (utilNum * pktLength) / curBandSwitchToSink
        avgDelay = calculateAvgDelay(nSource, bandSrcToSwitch, curBandSwitchToSink, pktLength, source, simTime)
        x.append(Ufactor)
        y.append(avgDelay)
        print(Ufactor, " ", avgDelay)
        if (Ufactor > 1):
            curBandSwitchToSink = curBandSwitchToSink + (bandSwitchToSinkhigh - bandSwitchToSinklow) / 200
        else:
            curBandSwitchToSink = curBandSwitchToSink + (bandSwitchToSinkhigh - bandSwitchToSinklow) / 150

    # plotting curve
    plt.plot(x, y)
    plt.xlabel("Utilization Factor")
    plt.ylabel("Average Delay")
    plt.title("Average Delay vs Utilization Factor")
    plt.show()


if __name__ == "__main__":
    main()