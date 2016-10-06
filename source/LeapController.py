'''
@author: xdobes13
'''


import Globals as globs
from Debug import dbg
import sys

__LeapSupported = None

try:
    sys.path.insert(0, globs.LEAP_LIBS_PATH)
    import Leap
    from Leap import Vector
    __LeapSupported = True
except ImportError as e:
    __LeapSupported = False
    dbg("Cannot import LeapMotion libraries.")


def isLeapSupported():
    ''' Returns True if LeapMotion platform is supported, returns False if not, returns None if unknown '''
    global __LeapSupported
    return __LeapSupported


try:
    class LeapController(Leap.Listener):
        '''
        Receives user input from LeapMotion, updates ControllerAggregator
        '''
        MIN_TIME_VISIBLE = 0.0#15
        SEARCH_WINDOW = 70 # In how many last frames to search for rotation
        MIN_WINDOW_SIZE = 10
        FACTOR_ROTX = 3
        FACTOR_ROTY = 1
        FACTOR_ROTZ = 1
        MIN_GRAB_STRENGTH = 0.2
        CROP_ROT_MIN = 0.02
        
        POS_X_SCALE = 0.1
        POS_X_LINEAR = 0
        
        POS_Y_SCALE = 0.1
        POS_Y_LINEAR = -25
        
        POS_Z_SCALE = -0.1
        POS_Z_LINEAR = 0
        
    
        def __init__(self, aggregator):
            '''
            aggregator = the ControllerAggregator object to report to
            '''
            self.__ca = aggregator
            self.__LeapController = Leap.Controller()
            Leap.Listener.__init__(self)
            self.__LeapController.add_listener(self)
            
        
        def on_connect(self, controller):
            dbg("Leap controller connected...")
            self.__ca.addSource("leap")
            controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
            
            
        def on_frame(self, controller):
            #print "Frame available"
            frame = controller.frame()
            if not frame.is_valid:
                self.__ca.invalidatePointer() # TODO Maybe not?
                return
            #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
            #  frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        
            if len(frame.hands) != 1: # User can only point into the cube with 1 hand
                self.__ca.invalidatePointer()
            
            # Is image stabilised?
            for hand in frame.hands:
                if hand.time_visible < self.MIN_TIME_VISIBLE: #TODO: What are the time units? seconds?
                    self.__ca.invalidatePointer()
                    return
        

                         
        
            # If we're grabbing, rotate the scene:

            
            # We're grabbing -> rotate:
            if self.__weReGrabbing(frame):
                # Get overall frame rotation:
                # Get latest valid frame:
                for i in range(self.SEARCH_WINDOW,0,-1):
                    start_frame = controller.frame(i)
                    if start_frame.is_valid:
                        break
                
                windowDistance = self.SEARCH_WINDOW - i
                if windowDistance < self.MIN_WINDOW_SIZE:
                    return # Window too short
                
                #windowFactor = self.SEARCH_WINDOW / windowDistance
                
                if not start_frame.is_valid:
                    return
                
                if not self.__weReGrabbing(start_frame):
                    return # We have to be grabbing on both frames to rotate
                
                # If the probability that user wanted to rotate is sufficient:
                #if frame.rotation_probability(start_frame) > 0.1:
                
                
                rotX = self.__cropRot(frame.rotation_angle(start_frame, Vector.x_axis) * self.FACTOR_ROTX)
                rotY = self.__cropRot(frame.rotation_angle(start_frame, Vector.y_axis) * self.FACTOR_ROTY)
                rotZ = self.__cropRot(frame.rotation_angle(start_frame, Vector.z_axis) * self.FACTOR_ROTZ)
                #dbg("Adding Rotation: " + str(-rotY) + ", " + str(-rotX) + ", " + str(rotZ))
                # TODO: modify by some factor
                self.__ca.addRotation(-rotY, -rotX, rotZ)
                self.__ca.invalidatePointer()
            
            else: # We're not grabbing:
                # If there is only 1 hand
                
                # Was there a gesture in the frame?
                if len(frame.gestures()) == 1:
                    for g in frame.gestures():
                        if g.is_valid and g.type is Leap.Gesture.TYPE_KEY_TAP:
                            key_tap = Leap.KeyTapGesture(g)
                            if (key_tap.pointable == frame.hands[0].fingers[1] and key_tap.direction.y < -0.8):
                                self.__ca.announcePlacement() # Announce placement request to CA
                                # TODO: delete after debugging:
                                keyTap = Leap.KeyTapGesture(g)
                                tap_point = keyTap.position
                                tapPointStr = "(" + str(tap_point.x) + ", " + str(tap_point.y) + ", " + str(tap_point.z) + ")"
                                tap_direction = keyTap.direction
                                tapDirStr = "(" + str(tap_direction.x) + ", " + str(tap_direction.y) + ", " + str(tap_direction.z) + ")"
                                dbg ("Detected key tap gesture at " + tapPointStr + " with direction " + tapDirStr)
                
                # Update pointer
                if ( len(frame.hands) == 1):
                    #ptrPos = frame.hands[0].stabilized_palm_position
                    ptrPos = frame.hands[0].palm_position
                    px = ptrPos.x * self.POS_X_SCALE + self.POS_X_LINEAR
                    py = ptrPos.y * self.POS_Y_SCALE + self.POS_Y_LINEAR
                    pz = ptrPos.z * self.POS_Z_SCALE + self.POS_Z_LINEAR
                    
                    #dbg("Palm position update: " + str(px) + ", " + str(pz) + ", " + str(py))
                    self.__ca.updatePointer(px, pz, py) #TODO: devide by some factor to fit Panda's coordinates
        
        
        def __weReGrabbing(self, frm):
            if len(frm.hands) != 2:
                #dbg("Not grabbing: Not 2 hands!")
                return False
            
            weReGrabbing = True
            for hand in frm.hands:
                if hand.grab_strength < self.MIN_GRAB_STRENGTH:
                    weReGrabbing = False
                    #dbg("Not grabbing: Weak grab! (" + str(hand.grab_strength) + ")")
                    break
            return weReGrabbing
        
        
        def __cropRot(self, rot):
            if ((rot > 0) and (rot < self.CROP_ROT_MIN)):
                return 0.0
            if ((rot < 0) and (rot > -self.CROP_ROT_MIN)):
                return 0.0
            return rot
        
            
except NameError as e:
    __LeapSupported = False
    dbg("LeapMotion not found, cannot define LM controller.")
            
    
    
        
