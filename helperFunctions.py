import time
import matplotlib.pyplot as plt

def printTopFive(applications, globalElapsed):

    # display current statistics
    print("Total Time Elapsed: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed)) + "\n")

    applications_sorted = {k: v for k, v in sorted(applications.items(), key=lambda x: x[1], reverse=True)}

    counter = 0
    for x in applications_sorted:
        print("Application Name: " + x)
        print("Time: " + time.strftime("%H:%M:%S", time.gmtime(applications_sorted[x])))
        percentage = 100 * applications_sorted[x] / globalElapsed
        print("Percent of Total Time: " + "%.2f" % percentage + "%\n")
        counter += 1
        if (counter > 4):
            break

def printAll(applications, globalElapsed):

    # display current statistics
    print("Total Time Elapsed: " + time.strftime("%H:%M:%S", time.gmtime(globalElapsed)) + "\n")

    applications_sorted = {k: v for k, v in sorted(applications.items(), key=lambda x: x[1], reverse=True)}

    for x in applications_sorted:
        print("Application Name: " + x)
        print("Time: " + time.strftime("%H:%M:%S", time.gmtime(applications_sorted[x])))
        percentage = 100 * applications_sorted[x] / globalElapsed
        print("Percent of Total Time: " + "%.2f" % percentage + "%\n")

def graphAll(applications):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = applications.keys()
    sizes = applications.values()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=None, labels=labels, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # add a circle at the center
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.show()