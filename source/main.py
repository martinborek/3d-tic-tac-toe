#!/usr/bin/env python2.7

'''
@author: xdobes13
'''

from ControllerAggregator import ControllerAggregator
import LeapController
import GameModel
import KeyboardController
from Debug import dbg
import sys

#import ViewBase
import ViewCube

if __name__ == '__main__':
    # Set up controllers:
    ca = ControllerAggregator()
    cKeyboard = KeyboardController.KeyboardController(ca)
    cLeap = None
     
    if (LeapController.isLeapSupported()):
        cLeap = LeapController.LeapController(ca)
        dbg("Leap is supported :-)")
    else:
        dbg("Leap is NOT supported :-(")
    
    # Set up Model:
    model = GameModel.Model(4, ca)
    
    if (len(sys.argv) == 2 and sys.argv[1] == "test"): # Load sample game
        model.playing_field = model.testing_field

    # Set up Panda:
    app = ViewCube.ViewCube(ca, model)
    #app = ViewBase.PandaApp(ca)
    
    model.setViewComponent(app)
    
    # Register keyboard controller with Panda:
    cKeyboard.setPandaSBase(app)
    
    app.run()
