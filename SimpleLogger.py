class SimpleLogger:
    def __init__(self, fileName):
        self.fileName = fileName
        self.initialized = False
        self.finalized = False

    def initialize(self):
        if( not self.initialized):
            self.fp = open(self.fileName, 'w')
            self.initialized = True
        else:
            print("Warning! Already initialized this logger")

    def finalize(self):
        if(self.initialized):
            self.fp.close()
            self.finalized = True
        else:
            print("Warning! Need to initialize this logger")

    def log(self, message):
        if(self.initialized and not self.finalized):
            self.fp.write(str(message) + "\n")
        else:
            print("Logger not initialized or already finalized")