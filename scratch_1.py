import time
from threading import Thread

def timer():
    count = 0
    while True:
        time.sleep(1)
        count += 1
        print("This program has now been running for " + str(count) + " minutes.")


background_thread = Thread(target=timer, args=())
background_thread.start()
while True:

    print("Hello! Welcome to the program timer!")
    name = input("What is your name?")
    print("Nice to meet you, " + name + "!")
