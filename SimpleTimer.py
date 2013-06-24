import time

class SimpleTimer:
    def __init__(self):
        self.started = False
        self.time = -1


    def start(self):
        if( not self.started):
            self.time = time.time()
            self.started = True
            return("Started timer.")
        else:
            print("Warning! Already started timer")

    def stop(self):
        if(self.started):
            result = time.time() - self.time
            self.time = -1
            self.started = False
            return("That took " + str(result) + " seconds.")
        else:
            print("Warning! Need to start timer")