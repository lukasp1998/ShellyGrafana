#import sched, time
import schedule, time
from shellyGetData import run
from detectShellysFromNetwork import run
from helperFunction import log, setDebug

def getShellyDataIntoDatabase():
    # run function from shellyGetData
    log("getting Data from Shellys")
    run()
    log("Done getting Data from Shellys")

def detectShellys():
    # run function from detectShellysFromNetwork
    log("Detecting Shellys")
    run()
    log("Done Detecting Shellys")

def scheduling():
    schedule.every(30).seconds.do(getShellyDataIntoDatabase)
    schedule.every(5).minutes.do(detectShellys)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    setDebug(True)
    detectShellys()
    log("starting Scheduling")
    scheduling()


