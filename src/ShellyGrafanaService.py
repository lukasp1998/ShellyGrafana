import schedule, time
import threading
import shellyGetData
import detectShellysFromNetwork
from helperFunction import log, setDebug

def getShellyDataIntoDatabase():
    # run function from shellyGetData
    log("getting Data from Shellys")
    shellyGetData.run()
    log("Done getting Data from Shellys")

def detectShellys():
    # run function from detectShellysFromNetwork
    log("Detecting Shellys")
    t1 = threading.Thread(target=detectShellysFromNetwork.run())
    t1.start()
    log("Done Detecting Shellys")

def scheduling():
    schedule.every(30).seconds.do(getShellyDataIntoDatabase)
    schedule.every(15).minutes.do(detectShellys)
    log("running State")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    setDebug(True)
    detectShellys()
    log("starting Scheduling")
    scheduling()


