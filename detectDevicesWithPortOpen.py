from socket import *
import time
import os
import json

clients = []

# Network Scanner to detect Devices with open Ports
def networkScan(subnet, startIp, endIp, startPort, endPort):
    startTime = time.time()
    for ipNr in range(startIp, endIp):

        t_IP = gethostbyname(subnet + str(ipNr))
        print('Starting scan on host: ', t_IP)

        for i in range(startPort, endPort+1):

            s = socket(AF_INET, SOCK_STREAM)

            s.settimeout(3)
            conn = s.connect_ex((t_IP, i))
            if (conn == 0):
                print('Port %d: OPEN' % (i,))
                clients.append(t_IP)
            s.close()
    print('Time taken:', time.time() - startTime)
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

    subnet = config["config"][0]["network"]["subnet"]
    startIp = config["config"][0]["network"]["ipRangeStart"]
    endIp = config["config"][0]["network"]["ipRangeEnd"]
    startPort = 80
    endPort = 80

    networkScan(subnet, startIp, endIp, startPort, endPort)

    safeClientsToFile(clients)