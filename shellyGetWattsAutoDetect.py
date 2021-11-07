import json
import requests
import os
from influxdb import InfluxDBClient


clients = []
dataList = []

# get Shellys from the List of Clients
# get JSON from webserver and Test for "wifi_sta"
def getDataFromShellys():
    for client_ip in clients:
        try:
            r = requests.get('http://' + client_ip + '/status')
            if r:
                if r.text.find("wifi_sta", 0, len(r.text)) >=0:
                    ip = r.json()["wifi_sta"]["ip"]
                    mac = r.json()["mac"]
                    updateCheck = r.json()["update"]["has_update"]
                    if updateCheck == 1:
                        updateCheck = 1
                    else:
                        updateCheck = 0

                    # get Shelly Style, 1 or multiple meters/emeters
                    # CODE MUST BE OPTIMIZED FOR AUTO powerData CREATION
                    if r.text.find("emeters", 0, len(r.text)) >=0:
                        for emeter in range(0, len(r.json()["emeters"])):
                            watts = []
                            voltage = []
                            watts.append(r.json()["emeters"][emeter]["power"])
                            voltage.append(r.json()["emeters"][1]["voltage"])

                            if len(watts) == 2:
                                powerData = [
                                    {
                                        "measurement": "shelly_watts",
                                        "tags": {
                                            "mac": mac
                                        },
                                        "fields": {
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
                                            "mac": mac
                                        },
                                        "fields": {
                                            "ip": ip,
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
                        power = r.json()["meters"][0]["power"]
                        powerData = [
                            {
                                "measurement": "shelly_watts",
                                "tags": {
                                    "mac": mac
                                },
                                "fields": {
                                    "ip": ip,
                                    "updateCheck": float(updateCheck),
                                    "watts": float(power)
                                }
                            }
                        ]
                        dataList.append(powerData)

                else:
                    print("NOT A SHELLY: " + client_ip)
            else:
                print("NOT A SHELLY: " + client_ip)


        except requests.exceptions.RequestException as e:
            print("Error on Device: ")


def readClientsFromFile(filePath):
    try:
        with open(filePath, "r") as txt_file:
            for line in txt_file.readlines():
                clients.append(line.replace('\n',''))
    except FileNotFoundError as e:
        print("NO CLIENTS FILE FOUND!")
    except EnvironmentError as e:
        print("ooOOOPS " + e)


def sendDataToInflux(ipAddress, port, username, password, database):
    client = InfluxDBClient('localhost', port, username, password, database)
    for data in dataList:
        client.write_points(data)

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
    print(config)

    readClientsFromFile(workingDirectory + '/clients.json')

    getDataFromShellys()

    # InFluxDB Connection
    ipAddress = config["config"][0]["database"]["address"]
    port = config["config"][0]["database"]["port"]
    username = config["config"][0]["database"]["username"]
    password = config["config"][0]["database"]["password"]
    database = config["config"][0]["database"]["database"]
    sendDataToInflux(ipAddress, port, username, password, database)


    print(dataList)
