import time
import threading
from queue import Queue
from collections import defaultdict

networkDiameter = 10
startSimTime = time.time()

class Packet:
    def __init__(self, src, dest, seq_no):
        self.src = src
        self.dest = dest
        self.seq_no = seq_no
        self.ttl_left = 5  # time to live in seconds
        self.startTime = 0
        self.nodesVisited = set()
        self.maxhopCount = networkDiameter
        self.maxRetransmit = 3


class Node:
    def __init__(self, id):
        self.nbrs = []
        self.floodedPackets = set()
        self.id = id


# Global entities
nodes = defaultdict(Node)
packets = {}
reached = defaultdict(bool)
dropped = defaultdict(bool)

noNodes = 1000
noPackets = 1000


def bfs(src, dest, seq_no):
    q = Queue()
    q.put(src)
    packets[seq_no].nodesVisited.add(src)

    while not q.empty():
        curN = q.get()

        if curN == dest:
            reached[seq_no] = True
            print(f"Destination reached (Node: {dest})")
            break

        curTimeInSeconds = time.time() - startSimTime
        print(f"Packet: {seq_no}, Received at Node: {curN} at : {curTimeInSeconds:.2f}s")

        if packets[seq_no].ttl_left < (curTimeInSeconds - packets[seq_no].startTime):
            print(f"Dropping Packet {seq_no} due to exceeding TTL")
            dropped[seq_no] = True
            break

        if packets[seq_no].maxhopCount == 0:
            print(f"Dropping Packet {seq_no} due to exhausting HopCount")
            dropped[seq_no] = True
            break

        if seq_no not in nodes[curN].floodedPackets:
            nodes[curN].floodedPackets.add(seq_no)
            print(f"From Node: {curN}, we are ...")

            for i in nodes[curN].nbrs:
                if i not in packets[seq_no].nodesVisited:
                    q.put(i)
                    print(f"Flooding to Node: {i}")
                    packets[seq_no].nodesVisited.add(i)
                else:
                    print(f"Sequence no: {seq_no} has visited Node: {i} before")

        else:
            print("Already Flooded!")


def routingIndividualPkt_lvl1(pkt):
    while not reached[pkt.seq_no] and not dropped[pkt.seq_no]:
        pkt.startTime = time.time() - startSimTime
        print(f"\nSending Packet: {pkt.seq_no} at: {pkt.startTime:.2f}s\n")
        bfs(pkt.src, pkt.dest, pkt.seq_no)

        if reached[pkt.seq_no]:
            print(f"\nPacket: {pkt.seq_no} has been successfully received!")

    if dropped[pkt.seq_no]:
        time.sleep(1)
        if pkt.maxRetransmit > 0:
            print(f"\nRetransmitting Packet: {pkt.seq_no}")
            pkt.maxRetransmit -= 1
            routingIndividualPkt_lvl1(pkt)
        else:
            print(f"\nRetransmits for Packet: {pkt.seq_no} exhausted!")


def isAlreadyNbr(nodeToCheck, nodeParent):
    return nodeToCheck in nodes[nodeParent].nbrs


def main():
    userChoice = int(input("\nDo you want to load PreBuilt Network for this simulation? If yes -> 1, If no -> 0 \n"))

    if not userChoice:
        noNodes = int(input("\nEnter network size (no of nodes): "))
        noPackets = int(input("\nEnter no of packets: "))

        for i in range(noNodes):
            nodes[i] = Node(i)
            nbrsSize = int(input(f"\nEnter No of New Neighbours for Node: {i} \n"))
            for _ in range(nbrsSize):
                tempNbr = int(input(f"\nEnter Neigbhour for Node {i}: "))
                if not isAlreadyNbr(tempNbr, i):
                    nodes[i].nbrs.append(tempNbr)
                    nodes[tempNbr].nbrs.append(i)

        for i in range(noPackets):
            src = int(input(f"\nEnter Source Node for Packet {i}: "))
            dest = int(input(f"\nEnter Destination Node for Packet {i}: "))
            packets[i] = Packet(src, dest, i)

    else:
        # Prebuilt network
        for i in range(6):
            nodes[i] = Node(i)

        nodes[0].nbrs = [1, 2, 4]
        nodes[1].nbrs = [0, 5]
        nodes[2].nbrs = [0, 4]
        nodes[3].nbrs = [4]
        nodes[4].nbrs = [0, 3, 5]
        nodes[5].nbrs = [1, 4]

        packets[0] = Packet(0, 5, 0)
        packets[1] = Packet(1, 4, 1)
        packets[2] = Packet(2, 3, 2)

    threads = []
    startSimTime = time.time()

    for i in range(3):
        print(f"\nAssigning new Thread for Packet: {i} .... \n")
        t = threading.Thread(target=routingIndividualPkt_lvl1, args=(packets[i],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    endSimTime = time.time()
    print(f"\n\nTotal Simulation time: {endSimTime - startSimTime:.2f}s\n")


if __name__ == "__main__":
    main()
