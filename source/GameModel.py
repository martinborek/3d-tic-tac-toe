# @author: xborek08
# -*- coding: utf-8 -*-

class Marks:
    '''Values used in playing field's cells.'''

    EMPTY = 1
    PLAYER_ONE = 2
    PLAYER_TWO = 3 


class Model:
    '''Game model. Contains game logic and playing field state.'''

    def __init__(self, size, ca):
        self.refresh = False
        self.__ca = ca
        self.__view = None
        self.__player = Marks.PLAYER_ONE

        self.size = size # Size of playing field
        self.playing_field = ([[[Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY]],
            [[Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY]],
            [[Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY]],
            [[Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY]]])
        
        self.testing_field = ([[[Marks.EMPTY, Marks.PLAYER_ONE, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.PLAYER_TWO],
            [Marks.EMPTY, Marks.PLAYER_TWO, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.PLAYER_TWO, Marks.EMPTY]],
            [[Marks.PLAYER_TWO, Marks.PLAYER_ONE, Marks.EMPTY, Marks.EMPTY],
            [Marks.PLAYER_TWO, Marks.EMPTY, Marks.EMPTY, Marks.PLAYER_TWO],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.PLAYER_ONE, Marks.EMPTY, Marks.EMPTY]],
            [[Marks.PLAYER_TWO, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.PLAYER_ONE, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.PLAYER_TWO, Marks.EMPTY, Marks.EMPTY],
            [Marks.PLAYER_TWO, Marks.PLAYER_ONE, Marks.EMPTY, Marks.EMPTY]],
            [[Marks.EMPTY, Marks.PLAYER_ONE, Marks.EMPTY, Marks.PLAYER_ONE],
            [Marks.PLAYER_TWO, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.EMPTY, Marks.EMPTY, Marks.EMPTY],
            [Marks.EMPTY, Marks.PLAYER_ONE, Marks.EMPTY, Marks.EMPTY]]])
        
        ca.registerPlacementListener(self.placementListener)

    def getMark(self, x, y, z):
        '''Returns mark from given position.'''

        if (x>=self.size or y>=self.size
                or z>=self.size or x<0 or y<0 or z<0):
            return False

        else:
            return self.playing_field[x][y][z]

    def setMark(self, x, y, z, mark):
        '''Sets mark at given position.'''

        self.refresh = True

        if (x>=self.size or y>=self.size
                or z>=self.size or x<0 or y<0 or z<0):
            return False

        elif self.playing_field[x][y][z] is not Marks.EMPTY:
            return False

        else:
            self.playing_field[x][y][z] = mark
            return True;
    
    def placementListener(self):
        (x, y, z) = self.__view.getSelectedCoords()
        #print(x)
        #print(y)
        #print(z)
        if (self.setMark(x, y, z, self.__player)):
            if (self.__player == Marks.PLAYER_ONE):
                self.__player = Marks.PLAYER_TWO
            else:
                self.__player = Marks.PLAYER_ONE
        
        
    def setViewComponent(self, view):
        self.__view = view
        
    def getPlayer(self):
        if (self.__player == Marks.PLAYER_ONE):
            return "červený"
        else:
            return "modrý"
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
