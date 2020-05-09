import time
from threading import Thread
from win32 import win32gui, win32api, win32console, win32process
import psutil
import atexit

def exitHandler():
    # print the time elapsed for the session
    print("\n")
    print("Total Time Elapsed: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed)) + "\n")
    for x in applications:
        print("Application Name: " + x + " Time: " + time.strftime("%H:%M:%S", time.gmtime(applications[x])))
        percentage = 100 * applications[x] / globalElapsed
        print("Percent of Total Time: " + "%.2f" % percentage + "%\n")

# go to exitHandler on exit
atexit.register(exitHandler)

def timer():
    previousApplicationName = ""
    currentApplicationStart = time.time()
    while True:

        # access the foreground window
        window = win32gui.GetForegroundWindow()
        processID = win32process.GetWindowThreadProcessId(window)
        if (psutil.pid_exists(processID[-1])):
            currentApplicationName = psutil.Process(processID[-1]).name()
        else:
            currentApplicationName = ""

        # checks if an application is opened
        if(currentApplicationName != previousApplicationName):
            currentApplicationElapsed = time.time() - currentApplicationStart
            # store the value into the dictionary
            if(applications.get(previousApplicationName) == None and previousApplicationName != ""):
                applications[previousApplicationName] = currentApplicationElapsed
            elif (previousApplicationName != ""):
                applications[previousApplicationName] += currentApplicationElapsed

            # record the current application start time
            currentApplicationStart = time.time()
            # update the previous application
            previousApplicationName = currentApplicationName

        time.sleep(1)


# all data is stored in dictionary 'applications'
applications = {}
backgroundThread = Thread(target=timer, args=( ))
backgroundThread.start()
start = time.time()
while True:
    keypressed = input()
    if(keypressed == 'q'):
        globalElapsed = time.time() - start
        print("Total Time Elapsed: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed)) + "\n")
        for x in applications:
            print("Application Name: " + x + " Time: " + time.strftime("%H:%M:%S", time.gmtime(applications[x])))
            percentage = 100 * applications[x] / globalElapsed
            print("Percent of Total Time: " + "%.2f" % percentage + "%\n")


