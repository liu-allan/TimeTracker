import time
import matplotlib.pyplot as plt
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
        globalElapsed = time.time() - start

        # display current statistics
        print("Total Time Elapsed: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed)) + "\n")

        applications_sorted = {k: v for k, v in sorted(applications.items(), key=lambda x: x[1], reverse=True)}

        counter = 0
        for x in applications_sorted:
            print("Application Name: " + x )
            print("Time: " + time.strftime("%H:%M:%S", time.gmtime(applications_sorted[x])))
            percentage = 100 * applications_sorted[x] / globalElapsed
            print("Percent of Total Time: " + "%.2f" % percentage + "%\n")
            counter += 1
            if (counter > 4):
                break

    # if user pressed t, print all the statistics
    elif(keypressed == 't'):
        globalElapsed = time.time() - start

        # display current statistics
        print("Total Time Elapsed: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed)) + "\n")

        applications_sorted = {k: v for k, v in sorted(applications.items(), key=lambda x: x[1], reverse=True)}

        for x in applications_sorted:
            print("Application Name: " + x)
            print("Time: " + time.strftime("%H:%M:%S", time.gmtime(applications_sorted[x])))
            percentage = 100 * applications_sorted[x] / globalElapsed
            print("Percent of Total Time: " + "%.2f" % percentage + "%\n")

    elif(keypressed == 'g'):
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = applications.keys()
        sizes = applications.values()

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode= None, labels= labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
