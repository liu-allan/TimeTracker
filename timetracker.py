import time
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
        print("Percent of Total: " + "%.2f" % percentage + "%\n")

start = time.time()
currentApplicationStart = start

# all data is stored in dictionary 'applications'
applications = {}
previousApplicationName = ""

# go to exitHandler on exit
atexit.register(exitHandler)

while True:

    #update the total elapsed time
    globalElapsed = time.time() - start

    # access the foreground window
    window = win32gui.GetForegroundWindow()
    processID = win32process.GetWindowThreadProcessId(window)
    currentApplicationName = psutil.Process(processID[-1]).name()

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

    time.sleep(10)



