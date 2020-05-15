import time
import matplotlib.pyplot as plt
from threading import Thread
from win32 import win32gui, win32api, win32console, win32process
import psutil

import helperFunctions

def timer():
    previousApplicationName = ""
    currentApplicationStart = time.time()
    while True:

        # access the foreground window
        window = win32gui.GetForegroundWindow()
        processID = win32process.GetWindowThreadProcessId(window)
        if (psutil.pid_exists(processID[-1])):
            # format application name
            currentApplicationName = psutil.Process(processID[-1]).name()
            currentApplicationName = currentApplicationName.capitalize()
            currentApplicationName = currentApplicationName.replace('.exe', '')
        else:
            currentApplicationName = ""

        # checks if an application is opened
        if(currentApplicationName != previousApplicationName):
            currentApplicationElapsed = time.time() - currentApplicationStart
            # store the value into the dictionary
            if(applications.get(previousApplicationName) == None and previousApplicationName != "" and previousApplicationName != "python.exe"):
                applications[previousApplicationName] = currentApplicationElapsed
            elif (previousApplicationName != "" and previousApplicationName != "python.exe"):
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

# main loop
while True:
    # poll user input
    keypressed = input()

    # if user pressed q, print the statistics for the 5 most used apps
    if(keypressed == 'q'):
        helperFunctions.printTopFive(start, applications)

    # if user pressed t, print all the statistics
    elif(keypressed == 't'):
        helperFunctions.printAll(start, applications)

    elif(keypressed == 'g'):
        helperFunctions.graphAll(applications)




