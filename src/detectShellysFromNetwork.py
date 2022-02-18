import threading
from socket import *
import time
import os
import requests
from helperFunction import *

# clients found to save Array
clients = []
# Debug Funktion, for Debug prints

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
    for ipNr in range(startIp, endIp+1):
        scanIp(ipNr, subnet, startPort, endPort, delay)
    log('Time taken:' + str(time.time() - startTime))


def safeClientsToFile(dataToSave):
    with open("../configs/clients.txt", "w") as txt_file:
        #for line in dataToSave:
        #    txt_file.write("".join(line) + "\n")
        txt_file.seek(0)
        for line in dataToSave:
            txt_file.write("".join(line) + "\n")
        txt_file.truncate()

def run():
    workingDirectory = os.getcwd()
    log('Working Directory ' + workingDirectory)
    config = readConfig("../configs/config.json")

    # AutoSubnet Detection missing
    subnet = config["config"][0]["network"]["subnet"]
    startIp = config["config"][0]["network"]["ipRangeStart"]
    endIp = config["config"][0]["network"]["ipRangeEnd"]
    startPort = config["config"][0]["network"]["port"]
    endPort = config["config"][0]["network"]["port"]
    delay = 1

    log("Subnet:" + str(subnet) + " | Port: " + str(startPort) + "-" + str(endPort) + " | IP Range: " + str(startIp) + "-" + str(endIp))

    networkScan(subnet, startIp, endIp, startPort, endPort, delay)
    safeClientsToFile(clients)

    log('Clients found: ' + str(clients))

if __name__ == '__main__':
    setDebug(True)
    run()