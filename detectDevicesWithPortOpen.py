import threading
from socket import *
import time
import os
import requests
from helperFunction import *

# clients found to save Array
clients = []
# Debug Funktion, for Debug prints
setDebug(True)

# Scan Device, if Port 80 open and request on /shelly contains json, add to clients
def scanIp(ipNr, subnet, startPort, endPort, delay):
        t_IP = gethostbyname(subnet + str(ipNr))
        #print('Starting scan on host: ', t_IP)
        log(t_IP)

        for i in range(startPort, endPort+1):

            s = socket(AF_INET, SOCK_STREAM)

            s.settimeout(delay)
            conn = s.connect_ex((t_IP, i))
            if (conn == 0):
                #print('Port %d: OPEN' % (i,))
                resp = requests.get('http://' + t_IP + '/shelly')
                if resp.headers.get('content-type') == 'application/json':
                    clients.append(t_IP)
                    log(t_IP)
            s.close()

# for loop throuw the given IpRange and calls the Scanner
# prints Time Needed for the Scan in Seconds
def networkScan(subnet, startIp, endIp, startPort, endPort, delay):
    startTime = time.time()
    for ipNr in range(startIp, endIp):
        scanIp(ipNr, subnet, startPort, endPort, delay)
    log('Time taken:' + str(time.time() - startTime))

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


    log(threads)
    # Starting threads
    for i in range(threadCount):
        threads[i].start()

    # Locking the main thread until all threads complete
    for i in range(threadCount):
        threads[i].join()

    log(clients)


def safeClientsToFile(dataToSave):
    with open("clients.txt", "w") as txt_file:
        for line in dataToSave:
            txt_file.write("".join(line) + "\n")

if __name__ == '__main__':
    workingDirectory = os.getcwd()
    log('Working Directory ' + workingDirectory)
    config = readConfig(workingDirectory + '/config.json')

# AutoSubnet Detection missing

    subnet = config["config"][0]["network"]["subnet"]
    startIp = config["config"][0]["network"]["ipRangeStart"]
    endIp = config["config"][0]["network"]["ipRangeEnd"]
    startPort = config["config"][0]["network"]["port"]
    endPort = config["config"][0]["network"]["port"]
    delay = 1

    networkScan(subnet, startIp, endIp, startPort, endPort, delay)
    ## NETWORK SCAN FAST NOT WORKING AT THE MOMENT
    #networkScanFast(subnet, startIp, endIp, startPort, endPort, delay)
    safeClientsToFile(clients)

    log('Clients found: ' + str(clients))