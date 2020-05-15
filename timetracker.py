import tkinter as tk
from win32 import win32gui, win32api, win32console, win32process
import psutil
import time
import helperFunctions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GUI:
    def __init__(self, master):

        self.master = master
        master.title("Time Tracker")

        master['bg'] = 'white'

        self.startStopButton = tk.Button(master, text="Start/Stop", command=lambda: timer(True)).pack()
        self.mostUsedButton = tk.Button(master, text="Most Used", command=lambda: helperFunctions.printTopFive(applications, globalElapsed)).pack()
        self.allButton = tk.Button(master, text="All", command=lambda: helperFunctions.printAll(applications, globalElapsed)).pack()

        pieChart = FigureCanvasTkAgg(figure, master)
        pieChart.get_tk_widget().pack()


figure = plt.Figure(figsize=(5, 5), dpi=100)
ax = figure.add_subplot(111)

# animate the usage of applications
def animate(interval):
    labels = applications.keys()
    sizes = applications.values()
    ax.clear()
    ax.pie(sizes)
    ax.legend(labels)
    ax.set_title('Usage')
    circle = plt.Circle((0, 0), 0.7, color='white')
    ax.add_artist(circle)

applications = {}
start = time.time()
currentApplicationStart = time.time()
previousApplicationName = ""
globalElapsed = start

def timer(toggle=False):
    global tracking_var
    global currentApplicationStart
    global previousApplicationName
    global globalElapsed

    if toggle:
        if tracking_var:
            tracking_var = False
        else:
            tracking_var = True

    if tracking_var:

        globalElapsed = time.time() - start

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
        if (currentApplicationName != previousApplicationName):
            currentApplicationElapsed = time.time() - currentApplicationStart
            # store the value into the dictionary
            if (applications.get(previousApplicationName) == None and previousApplicationName != ""):
                applications[previousApplicationName] = currentApplicationElapsed
            elif (previousApplicationName != ""):
                applications[previousApplicationName] += currentApplicationElapsed

            # record the current application start time
            currentApplicationStart = time.time()
            # update the previous application
            previousApplicationName = currentApplicationName

        root.after(1000, timer)


if __name__ == '__main__':
    root = tk.Tk()
    tracking_var = False
    timeTracker = GUI(root)
    ani = animation.FuncAnimation(figure, animate, interval=1000)
    root.mainloop()