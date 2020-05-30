import tkinter as tk
from win32 import win32gui, win32api, win32console, win32process
import psutil
import time
import helperFunctions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter.font import Font

class GUI:
    def __init__(self, master):

        self.master = master
        master.title("Time Tracker")
        master['bg'] = 'white'

        pieChart = FigureCanvasTkAgg(figure, master)
        pieChart.get_tk_widget().pack(side = "top", fill= "both", expand = 1)

        self.startStopButton = tk.Button(master, text="Start/Stop", command=lambda: self.start(True))
        self.startStopButton.pack(side = "left", fill="x", expand = 1)

        # self.mostUsedButton = tk.Button(master, text="Most Used", command=lambda: helperFunctions.printTopFive(applications, globalElapsed))
        # self.mostUsedButton.pack(side="left", fill="x", expand = 1)
        #
        # self.allButton = tk.Button(master, text="All", command=lambda: helperFunctions.printAll(applications, globalElapsed))
        # self.allButton.pack(side="left", fill="x", expand = 1)

        self.text = tk.StringVar()
        self.text.set("Stopped")
        self.runningLabel = tk.Label(master, textvariable = self.text)
        self.runningLabel.pack(side="left", fill = "both", expand=1)

    def start(self, toggle):
        timer(toggle)
        global running
        if toggle:
            if running:
                running = False
            else:
                running = True
        if running:
            self.text.set("Running")
        else:
            self.text.set("Stopped: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed)))

figure = plt.Figure(figsize=(6, 4), dpi=100)
ax = figure.add_subplot(111)

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        if(pct > 5):
            return time.strftime("%H:%M:%S", time.gmtime(val))
        else:
            return ''
    return my_autopct

# animate the usage of applications
def animate(interval):
    labels = applications.keys()
    sizes = applications.values()
    ax.clear()
    ax.pie(sizes, autopct=make_autopct(sizes), pctdistance=0.5, startangle=90)
    ax.legend(labels, bbox_to_anchor=(1.3, 1))
    ax.set_title('Application Usage')
    circle = plt.Circle((0, 0), 0.7, color='white')
    ax.add_artist(circle)


def timer(toggle=False):
    global tracking_var
    global currentApplicationStart
    global previousApplicationName
    global globalElapsed
    global text

    if toggle:
        if tracking_var:
            tracking_var = False
        else:
            tracking_var = True

    if tracking_var:
        text = "Running: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed))
        globalElapsed += 1

        # access the foreground window
        window = win32gui.GetForegroundWindow()
        processID = win32process.GetWindowThreadProcessId(window)
        if (psutil.pid_exists(processID[-1])):
            # format application name
            currentApplicationName = psutil.Process(processID[-1]).name()
            currentApplicationName = currentApplicationName.capitalize()
            currentApplicationName = currentApplicationName.replace('.exe', '')
            if(currentApplicationName == "Python"):
                currentApplicationName = "Time Tracker"
        else:
            currentApplicationName = "Unknown"

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

applications = {}
start = time.time()
currentApplicationStart = time.time()
previousApplicationName = ""
globalElapsed = 0

if __name__ == '__main__':
    tracking_var = False
    running = False
    root = tk.Tk()
    timeTracker = GUI(root)
    ani = animation.FuncAnimation(figure, animate, interval=1000)
    root.mainloop()