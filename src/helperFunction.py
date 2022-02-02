# helperFunction.py
import json

# logging Funktion to get prints Only when needed for Debugging Purpose
DEBUG = False
def setDebug(status):
    global DEBUG
    DEBUG = status

# Print Logging Message
def log(loggingMessage):
    if DEBUG:
        print(loggingMessage)

# JSON config reader for all JSON configs
def readConfig(filePath):
    try:
        with open(filePath, "r") as json_file:
            config = json.load(json_file)
            return config

    except FileNotFoundError as e:
        print("NO CONFIG FILE FOUND!")
    except EnvironmentError as e:
        print("ooOOOPS " + e)