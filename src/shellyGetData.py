import json
import requests
import os
from influxdb import *
from helperFunction import *

clients = []
dataList = []

# get Shellys from the List of Clients
# get JSON from webserver and Test for "wifi_sta"
def getDataFromShellys():
    for clientIp in clients:
        try:
            rStatus = requests.get('http://' + clientIp + '/status')
            log('IP= ' + clientIp)
            if rStatus:
                if rStatus.text.find("wifi_sta", 0, len(rStatus.text)) >=0:
                    ip = rStatus.json()["wifi_sta"]["ip"]
                    mac = rStatus.json()["mac"]
#                    temperature = rStatus.json()["temperature"]
                    updateCheck = rStatus.json()["update"]["has_update"]
                    if updateCheck == 1:
                        updateCheck = 1
                    else:
                        updateCheck = 0

                    try:
                        rSettings = requests.get('http://' + clientIp + '/settings')
                        if rSettings:
                            hostname = rSettings.json()["device"]["hostname"]
                            name = rSettings.json()["name"]

                    except requests.exceptions.RequestException as e:
                        print("Error on Device: " + clientIp)

                    # get Shelly Style, 1 or multiple meters/emeters
                    # CODE MUST BE OPTIMIZED FOR AUTO powerData CREATION
                    if rStatus.text.find("emeters", 0, len(rStatus.text)) >=0:
                        for emeter in range(0, len(rStatus.json()["emeters"])):
                            watts = []
                            voltage = []
                            watts.append(rStatus.json()["emeters"][emeter]["power"])
                            voltage.append(rStatus.json()["emeters"][1]["voltage"])

                            if len(watts) == 2:
                                powerData = [
                                    {
                                        "measurement": "shelly_watts",
                                        "tags": {
                                            "mac": mac,
                                            "name": name
                                        },
                                        "fields": {
                                            "ip": ip,
                                            "name": name,
                                            "hostname": hostname,
#                                            "temperature": float(temperature),
                                            "updateCheck": float(updateCheck),
                                            "watts": float(watts[0]),
                                            "voltage": float(voltage[0]),
                                            "watts2": float(watts[1]),
                                            "voltage2": float(voltage[1])
                                        }
                                    }
                                ]
                                dataList.append(powerData)

                            if len(watts) == 3:
                                powerData = [
                                    {
                                        "measurement": "shelly_watts",
                                        "tags": {
                                            "mac": mac,
                                            "name": name
                                        },
                                        "fields": {
                                            "ip": ip,
                                            "name": name,
                                            "hostname": hostname,
#                                            "temperature": float(temperature),
                                            "updateCheck": float(updateCheck),
                                            "watts": float(watts[0]),
                                            "voltage": float(voltage[0]),
                                            "watts2": float(watts[1]),
                                            "voltage2": float(voltage[1]),
                                            "watts3": float(watts[2]),
                                            "voltage3": float(voltage[2])
                                        }
                                    }
                                ]
                                dataList.append(powerData)
                    else:
                        power = rStatus.json()["meters"][0]["power"]
                        powerData = [
                            {
                                "measurement": "shelly_watts",
                                "tags": {
                                    "mac": mac,
                                    "name": name
                                },
                                "fields": {
                                    "ip": ip,
                                    "name": str(name),
                                    "hostname": hostname,
#                                    "temperature": float(temperature),
                                    "updateCheck": float(updateCheck),
                                    "watts": float(power)
                                }
                            }
                        ]
                        dataList.append(powerData)

                else:
                    print("NOT A SHELLY: " + clientIp)
            else:
                print("NOT A SHELLY: " + clientIp)


        except requests.exceptions.RequestException as e:
            print("Error on Device: " + clientIp)


def readClientsFromFile(filePath):
    try:
        with open(filePath, "r") as txt_file:
            for line in txt_file.readlines():
                clients.append(line.replace('\n',''))
    except FileNotFoundError as e:
        print("NO CLIENTS FILE FOUND!")
    except EnvironmentError as e:
        print("ooOOOPS, No Idea what happend!" + e)


def sendDataToInflux(ipAddress, port, username, password, database):
    try:
        client = InfluxDBClient('localhost', port, username, password, database)
        for data in dataList:
            client.write_points(data)
    except Exception as e:
        print("Database Error: " + str(e))

def readConfig(filePath):
    try:
        with open(filePath, "r") as json_file:
            config = json.load(json_file)
            return config

    except FileNotFoundError as e:
        print("NO CONFIG FILE FOUND!")
        exit()
    except EnvironmentError as e:
        print("ooOOOPS " + e)

def run():
    workingDirectory = os.getcwd()
    config = readConfig(workingDirectory + '/configs/config.json')

    readClientsFromFile(workingDirectory + '/configs/clients.txt')
    getDataFromShellys()
    log("Clients From File: " + str(clients))

    # InFluxDB Connection
    ipAddress = config["config"][0]["database"]["address"]
    port = config["config"][0]["database"]["port"]
    username = config["config"][0]["database"]["username"]
    password = config["config"][0]["database"]["password"]
    database = config["config"][0]["database"]["database"]

    ## TODO ad CODE to detect if DATABASE not found
    sendDataToInflux(ipAddress, port, username, password, database)
    log("DATALIST:" + str(dataList))

if __name__ == '__main__':
    setDebug(True)
    run()
