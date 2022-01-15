import threading
from socket import *
import time
import os
import json

clients = []

# Network Scanner to detect Devices with open Ports
def networkScan(subnet, startIp, endIp, startPort, endPort, delay):
    startTime = time.time()
    for ipNr in range(startIp, endIp):

        t_IP = gethostbyname(subnet + str(ipNr))
        #print('Starting scan on host: ', t_IP)

        for i in range(startPort, endPort+1):

            s = socket(AF_INET, SOCK_STREAM)

            s.settimeout(delay)
            conn = s.connect_ex((t_IP, i))
            if (conn == 0):
                #print('Port %d: OPEN' % (i,))
                clients.append(t_IP)
            s.close()
    print('Time taken:', time.time() - startTime)
    print(clients)

# Thread for Faster Network Scanner
def scanIpRangeThread(subnet, startIp, endIp, startPort, endPort, delay):
     clientList = []
     for ipNr in range(int(startIp), int(endIp)):
         t_IP = gethostbyname(subnet + str(ipNr))
         print('Starting scan on host: ', t_IP)

         for i in range(startPort, endPort + 1):

             s = socket(AF_INET, SOCK_STREAM)

             s.settimeout(delay)
             conn = s.connect_ex((t_IP, i))
             if (conn == 0):
                 print('Port %d: OPEN' % (i,))
                 clientList.append(t_IP)
             s.close()
     #for ip in clientList:
     #    clients.append(ip)
     #clients.insert(clientList)
     clients.extend(clientList)

# Faster Mutithreaded Network Scan
### TODO
def networkScanFast(subnet, startIp, endIp, startPort, endPort, delay):
    threads = []  # To run TCP_connect concurrently
    output = {}  # For printing purposes
    threadCount = 4
    # Spawning threads to scan ports
    #for i in range(threadCount):
    #    t = threading.Thread(target=scanIpRangeThread, args=(subnet, startIp, endIp, startPort, endPort, delay))
    #    threads.append(t)

    t1 = threading.Thread(target=scanIpRangeThread, args=(subnet, 2, 64, startPort, endPort, delay))
    t2 = threading.Thread(target=scanIpRangeThread, args=(subnet, 65, 127, startPort, endPort, delay))
    t3 = threading.Thread(target=scanIpRangeThread, args=(subnet, 125, 189, startPort, endPort, delay))
    t4 = threading.Thread(target=scanIpRangeThread, args=(subnet, 190, 250, startPort, endPort, delay))

    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)


    print(threads)
    # Starting threads
    for i in range(threadCount):
        threads[i].start()

    # Locking the main thread until all threads complete
    for i in range(threadCount):
        threads[i].join()

    print(clients)


def safeClientsToFile(dataToSave):
    with open("clients.txt", "w") as txt_file:
        for line in dataToSave:
            txt_file.write("".join(line) + "\n")
    #save("clients", dataToSave)

def readConfig(filePath):
    try:
        with open(filePath, "r") as json_file:
            config = json.load(json_file)
            return config

    except FileNotFoundError as e:
        print("NO CONFIG FILE FOUND!")
    except EnvironmentError as e:
        print("ooOOOPS " + e)


if __name__ == '__main__':
    workingDirectory = os.getcwd()
    print(workingDirectory)
    config = readConfig(workingDirectory + '/login.json')

# AutoSubnet Detection missing

    subnet = config["config"][0]["network"]["subnet"]
    startIp = config["config"][0]["network"]["ipRangeStart"]
    endIp = config["config"][0]["network"]["ipRangeEnd"]
    startPort = 80
    endPort = 80
    delay = 1

    networkScan(subnet, startIp, endIp, startPort, endPort, delay)
    ## NETWORK SCAN FAST NOT WORKING AT THE MOMENT
    #networkScanFast(subnet, startIp, endIp, startPort, endPort, delay)
    safeClientsToFile(clients)