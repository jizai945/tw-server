import os
import threading
import queue
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler

class ULOG(threading.Thread):
    AQueue = queue.Queue(100000)
    nPID = os.getpid()
    Adt = datetime.datetime.now().strftime('%Y%m%d')
    nCount = 1
    
    def __init__(self, threadID, name, module, logLevel):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.module = module

        try:
            os.makedirs('./log') 
        except:
            pass
        print("set loglevel: [%s]" % (logLevel) )
        formatter = logging.Formatter('%(asctime)s|%(name)s|%(process)d|%(levelname)s|%(message)s')
        # logfile = "log_" + self.module + "_" + str(logging2.nPID) + "_" + str(logging2.Adt) + ".log"
        logfile = "log/log_" + self.module + "_" + str(ULOG.Adt) + ".log"
        self.logger = logging.getLogger(__name__)
        
        self.rHandler = RotatingFileHandler(logfile, maxBytes = 10*1024*1024, backupCount = 10, encoding='utf-8')
        self.rHandler.setFormatter(formatter)
        
        self.console = logging.StreamHandler()    
        self.console.setFormatter(formatter)
        
        if logLevel == 'DEBUG' :
            self.logger.setLevel(level = logging.DEBUG)
            self.rHandler.setLevel(logging.DEBUG)
            self.console.setLevel(logging.DEBUG)
        elif logLevel == 'INFO' :
            self.logger.setLevel(level = logging.INFO)
            self.rHandler.setLevel(logging.INFO)
            self.console.setLevel(logging.INFO)
        elif logLevel == 'WARNING' :
            self.logger.setLevel(level = logging.WARN)
            self.rHandler.setLevel(logging.WARN)
            self.console.setLevel(logging.WARN)
        elif logLevel == 'ERROR' :
            self.logger.setLevel(level = logging.ERROR)
            self.rHandler.setLevel(logging.ERROR)
            self.console.setLevel(logging.ERROR)        

        self.logger.addHandler(self.rHandler)
        self.logger.addHandler(self.console)        

    #????????????????????????????????????????????????
    def reSetLog(self):
        AdtTemp = datetime.datetime.now().strftime('%Y%m%d')
        #??????????????????
        if AdtTemp == ULOG.Adt:
            return(True)
            
        ULOG.Adt = AdtTemp
        logfile = "log_" + self.module + "_" + str(ULOG.nPID) + "_" + str(AdtTemp) + ".log"
        self.rHandler = RotatingFileHandler(logfile, maxBytes = 1*1024, backupCount = 10)
        
        self.logger.addHandler(self.rHandler)
        self.logger.addHandler(self.console)    
        ULOG.nCount += 1
        
    def run(self):
        print ("?????????????????????" + self.name)

        while True:
            #???????????????????????????
            data = ULOG.AQueue.get()
            if type(data) == type("") and data == "EXIT":
                print('logging exit')
                return

            self.reSetLog()
            #???????????????????????????????????????????????????
            print(data)
            level = list(data.keys())[0]
            content = data.get(level)
            #?????????????????????|?????????list????????????
            lstContent = list(content.split('|'))
            if level == 'DEBUG' :
                self.logger.debug(*lstContent)
            elif level == 'INFO' :
                self.logger.info(*lstContent)
            elif level == 'WARNING' :
                self.logger.warn(*lstContent)
            elif level == 'ERROR' :
                self.logger.error(*lstContent)

        print ("???????????????" + self.name)    
    
def debug(*content):    
    logMsg = ""
    #??????????????????????????????????????????
    for i in range(len(content)):
        if i == len(content)-1:
            logMsg += content[i]
        else:
            logMsg += content[i]+"|"
    ULOG.AQueue.put({'DEBUG':logMsg})
            
def info(*content):
    logMsg = ""
    for i in range(len(content)):
        if i == len(content)-1:
            logMsg += content[i]
        else:
            logMsg += content[i]+"|"
    ULOG.AQueue.put({'INFO':logMsg})
                
def warn(*content):
    logMsg = ""
    for i in range(len(content)):
        if i == len(content)-1:
            logMsg += content[i]
        else:
            logMsg += content[i]+"|"
    ULOG.AQueue.put({'WARNING':logMsg})
        
def error(*content):
    logMsg = ""
    for i in range(len(content)):
        if i == len(content)-1:
            logMsg += content[i]
        else:
            logMsg += content[i]+"|"
    ULOG.AQueue.put({'ERROR':logMsg})

def exit():
    print('log req exit')
    ULOG.AQueue.put('EXIT')
      
def init(module, level):
    # ???????????????
    thread1 = ULOG(1, "Thread-log", module, level)
    # ???????????????
    thread1.start()
#    thread1.join()