'''
xdobes13

Aggregates various user inputs into a unified module
'''

import threading

class ControllerAggregator(object):
    ''' Unified interface for all controller inputs '''
    
    def __init__(self):
        self.__lock = threading.RLock() # internal reentrant lock for synchronizing access
        self.__newData = False  # internal flag to indicate new data
        
        self.__sources = [] # Array of strings -> names of input sources (keyboard, leap)
        
        self.__rotX = 0.0
        self.__rotY = 0.0
        self.__rotZ = 0.0
        
        self.__ptrX = 0.0
        self.__ptrY = 0.0
        self.__ptrZ = 0.0
        self.__ptrValid = False
        
        self.__placementCallbackFn = self.__nop
        
        
    def registerPlacementListener(self, callbackFunction):
        ''' Registers a function that will be called when user requests to place a mark '''
        with(self.__lock):
            self.__placementCallbackFn = callbackFunction
        
        
    def __nop(self): # NOP function for initial callback
        return
    
    
    def hasNewData(self):
        with(self.__lock):
            return self.__newData
    
    
    def getRotation(self):
        ''' Returns a tuple with rotation (x,y,z) since last call to resetRot() '''
        with(self.__lock):
            self.__newData = False
            return (self.__rotX, self.__rotY, self.__rotZ)
    
    
    def resetRotation(self):
        ''' Resets rotation to zero '''
        with(self.__lock):
            self.__newData = False
            self.__rotX = 0.0
            self.__rotY = 0.0
            self.__rotZ = 0.0
    
    
    def isPointerValid(self):
        return self.__ptrValid
    
    
    def getPointer(self):
        ''' Returns a tuple with pointer coordinates relative to the camera (x,y,z) '''
        with(self.__lock):
            self.__newData = False
            return (self.__ptrX, self.__ptrY, self.__ptrZ)
        
    def getSources(self):
        with(self.__lock):
            self.__newData = False
            return self.__sources
    
    
    def addRotation(self, rotX, rotY, rotZ):
        with(self.__lock):
            self.__newData = True
            self.__rotX += rotX
            self.__rotY += rotY
            self.__rotZ += rotZ

    
    def updatePointer(self, ptrX, ptrY, ptrZ): #TODO
        with(self.__lock):
            self.__newData = True
            self.__ptrX = ptrX
            self.__ptrY = ptrY
            self.__ptrZ = ptrZ
            self.__ptrValid = True
            
            
    def invalidatePointer(self):
        with(self.__lock):
            self.__newData = True
            self.__ptrValid = False
        
            
    def addSource(self, source):
        with(self.__lock):
            self.__newData = True
            self.__sources.append(source)
            
    def announcePlacement(self):
        with(self.__lock):
            self.__placementCallbackFn() # Announce placement request by calling callback
            