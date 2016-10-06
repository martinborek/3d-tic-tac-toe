'''
@author: xdobes13
'''

import time
import threading

class KeyboardController(object):
    '''
    Receives keyboard input from Panda, updates ControllerAggregator
    '''


    def __init__(self, aggregator):
        '''
        aggregator = the ControllerAggregator object to report to
        '''
        self.__ca = aggregator
        self.__ca.addSource("keyboard")
        self.__sBase = None
        
        # Flags for pressed keys:
        self.__kf = {'a' : False,
                    's' : False,
                    'w' : False,
                    'd' : False,
                    'q' : False,
                    'e' : False,
                    ' ' : False }
        
        
        
    def setPandaSBase(self, sBase):
        '''
        Required in order for the controller to work.  
        SBase = the ShowBase object of the Panda app. Can only be done once. 
        '''
        if self.__sBase is not None:
            return # Only allow to set SBase once.
        
        self.__sBase = sBase
        
        # Now register for key events:
        sBase.accept('a', self.__setKF, ['a', True])
        sBase.accept('s', self.__setKF, ['s', True])
        sBase.accept('w', self.__setKF, ['w', True])
        sBase.accept('d', self.__setKF, ['d', True])
        sBase.accept('q', self.__setKF, ['q', True])
        sBase.accept('e', self.__setKF, ['e', True])
        sBase.accept('space', self.__setKF, [' ', True])
        
        sBase.accept('a-up', self.__setKF, ['a', False])
        sBase.accept('s-up', self.__setKF, ['s', False])
        sBase.accept('w-up', self.__setKF, ['w', False])
        sBase.accept('d-up', self.__setKF, ['d', False])
        sBase.accept('q-up', self.__setKF, ['q', False])
        sBase.accept('e-up', self.__setKF, ['e', False])
        
        # Start thread to perform changes to CA:
        self.__thread = threading.Thread(target=self.__actionThread)
        self.__thread.setDaemon(True)
        self.__thread.start()
    
    
    def __setKF(self, key, value):
        ''' Sets a flag for given key '''
        self.__kf[key] = value
    
        
    def __actionThread(self):
        ''' Updates CA in given time intervals, based on key flags '''
        while True:
            if self.__kf['a']:
                self.__ca.addRotation(2,0,0)
            
            if self.__kf['s']:
                self.__ca.addRotation(0,-2,0)
            
            if self.__kf['w']:
                self.__ca.addRotation(0,2,0)
            
            if self.__kf['d']:
                self.__ca.addRotation(-2,0,0)
            
            if self.__kf['q']:
                self.__ca.addRotation(0,0,-2)
            
            if self.__kf['e']:
                self.__ca.addRotation(0,0,2)
                
            if self.__kf[' ']: # Spacebar
                self.__kf[' '] = False # One time only
                self.__ca.announcePlacement() # Announce placement to CA
                
                
            time.sleep(0.02)
        
        
        
        
        
        
        
        
