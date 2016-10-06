# @author: xborek08
# -*- coding: utf-8 -*-
import sys
from panda3d.core import *
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
import GameModel
import math

#import CubeModel

class ViewCube(ShowBase):
    '''View containing main cube with grid and marks.'''

    def __init__(self, ctrlAggregator, model):
        
        ShowBase.__init__(self)
        self.ca = ctrlAggregator
        self.model = model
        
        self.__ptrPos = [0,0,0];
 
        # Prepare heartbeat:
        self.running = False
    
        #Set fullscreen:
        props = WindowProperties()
        
        #base.makeDefaultPipe()
        if not base.pipe.isValid():
            dbg("Panda3D reports that pipe is not valid. Quitting.")
            quit()    
        
        # Set Fullscreen:   
        #props.setSize(base.pipe.getDisplayWidth(), base.pipe.getDisplayHeight())
        #props.setFullscreen(True)
        #base.win.requestProperties(props)
        
        # Add the adjustCameraTask procedure to the task manager.
        self.taskMgr.add(self.move_pointer, "move_pointer")
        self.taskMgr.add(self.rotate, "rotate")
        self.taskMgr.add(self.refresh, "refresh")

        base.accept("escape", sys.exit)
        base.setBackgroundColor(0.0, 0.0, 0.0)
        base.disableMouse()
         
        #base.camLens.setNearFar(1.0, 50.0)
        #base.camLens.setFov(30.0)
         
        camera.setPos(0.0, -40.0, 0.0)
        camera.lookAt(0.0, 0.0, 0.0)
         

        self.pointer_node = self.render.attachNewNode("pointer_node")
        self.pointer_node.setPos(0.0, 0.0, 0.0)

        self.root_x_node = self.render.attachNewNode("RootX")
        self.root_x_node.setPos(0.0, 0.0, 0.0)

        self.aux_node = self.root_x_node.attachNewNode("Aux")
        self.aux_node.setPos(0.0, 0.0, 0.0)
        
        self.auxPtr_node = self.root_x_node.attachNewNode("Aux")
        self.auxPtr_node.setPos(0.0, 0.0, 0.0)

        self.root_node = self.root_x_node.attachNewNode("Root")
        self.root_node.setPos(0.0, 0.0, 0.0)

        self.big_cube_node = self.root_node.attachNewNode("Big cube")
        self.big_cube_node.setPos(0.0, 0.0, 0.0)
        self.big_cube_node.setTransparency(TransparencyAttrib.MDual)

        self.cube_node = self.root_node.attachNewNode("Cube")
        self.cube_node.setPos(0.0, 0.0, 0.0)

        self.marks_node = self.root_node.attachNewNode("Marks")
        self.marks_node.setPos(0.0, 0.0, 0.0)

        #render.setRenderModeWireframe()

        # COLORS & SHAPES
        self.cell_size = 2
        self.init_position = -(self.cell_size/4.0) * (self.model.size-1)

        self.big_cube_node.setAlphaScale(0.08)

        self.model_pointer = loader.loadModel("models/cube.egg")
        self.model_pointer.setScale(0.6, 0.6, 0.6)
        self.model_pointer.setTransparency(TransparencyAttrib.MDual, 1)
        self.pointer_color = VBase4(0, 1, 0, 1)
        
        self.model_pointerCube = loader.loadModel("models/cube.egg")
        self.model_pointerCube.setScale(self.cell_size, self.cell_size, self.cell_size)
        self.model_pointerCube.setTransparency(TransparencyAttrib.MDual, 1)
        self.pointer_colorCube = VBase4(1, 1, 0, 0.3)
        self.pointer_colorCubeEdge = VBase4(1, 1, 1, 1)
        
        #self.model_player_one = loader.loadModel("models/star.egg")
        #self.model_player_one.setScale(0.25, 0.25, 0.25)
        self.model_player_one = loader.loadModel("models/sphere.egg")
        self.model_player_one.setTransparency(TransparencyAttrib.MDual, 1)
        self.model_player_one.setScale(0.6, 0.6, 0.6)
        #self.model_player_two = loader.loadModel("models/cube.egg")
        #self.model_player_two.setScale(0.3, 0.3, 0.3)
        self.model_player_two = loader.loadModel("models/sphere.egg")
        self.model_player_two.setTransparency(TransparencyAttrib.MDual, 1)
        self.model_player_two.setScale(0.6, 0.6, 0.6)
        self.model_empty = loader.loadModel("models/cube.egg")
        self.model_empty.setTransparency(TransparencyAttrib.MDual, 1)
        self.model_empty.setScale(0.15, 0.15, 0.15)

        self.model_big_cube = loader.loadModel("models/cube.egg")
        self.model_big_cube.setTransparency(TransparencyAttrib.MDual, 1)
        bc_size = self.cell_size * self.model.size
        self.model_big_cube.setScale(bc_size, bc_size, bc_size)

        self.grid_color = VBase4(0.3, 0.3, 0.3, 1)
        self.grid_thickness = 1;

        self.big_cube_color = VBase4(1, 1, 1, 1)
        self.player_one_color = VBase4(1, 0, 0, 1)
        self.player_two_color = VBase4(0, 0, 1, 1)
        self.empty_color = VBase4(0.5, 0.5, 0.5, 1)

        self.cubes = []
        self.marks = []

        # POINTER
        self.pointer = self.model_pointer.copyTo(self.pointer_node)
        self.pointer.setColor(self.pointer_color)
        self.auxPtr_node.wrtReparentTo(self.pointer_node)
        
        # POINTER CUBE
        self.pointerCube_node = self.root_node.attachNewNode("PointerCube")
        self.pointerCube = self.model_pointerCube.copyTo(self.pointerCube_node)
        self.pointerCube.setColor(self.pointer_colorCube)
        cube = self.createCube(0, 0, 0,
                            self.cell_size, self.pointer_colorCubeEdge, 3)
        self.pointerCube_node.attachNewNode(cube)

        self.cubes = []
        self.marks = []
        self.big_cube = None

        self.big_cube = self.model_big_cube.copyTo(self.big_cube_node)
        self.big_cube.setColor(self.big_cube_color)
        self.big_cube.setPos(0, 0, 0)

        # DRAW
        self.drawPlayingField()
        
        # OSD
        # Add text node
        self.text = TextNode('textInfo')
        self.text.setText("default")
        self.textNodePath = aspect2d.attachNewNode(self.text)
        self.textNodePath.setScale(0.07)
        self.textNodePath.setPos((-1.2,0,-0.8))
        
        # SCENE LIGHTING:
        #self.plight = PointLight('plight')
        #self.plight.setColor(VBase4(1, 1, 1, 1))
        #self.plight.setAttenuation(Vec3( 0, 0, 0.001 ))
        
        #self.plnp = self.render.attachNewNode(self.plight)
        #self.plnp.setPos(0, 20, 8)
        #self.marks_node.setLight(self.plnp)
        
        
        #alight = AmbientLight('alight')
        #alight.setColor(VBase4(1,1,1,1))
        #alnp = self.render.attachNewNode(alight)
        #self.render.setLight(alnp)


    def drawPlayingField(self, redraw=False):
        '''Draws playing field - main cube containing grid (made of cubes)
        and marks. If redraw==True: Redraw marks and do not draw cubes'''

        if redraw:
            for mark in self.marks:
                mark.removeNode()
            self.marks = []

        #cube_node.setTransparency(TransparencyAttrib.MAlpha)
        #cube_node.setAlphaScale(0.6)
        for i in range(0, self.model.size):
            pos_x = (self.init_position + i) * 2 * self.cell_size

            for j in range(0, self.model.size):
                pos_y = (self.init_position + j) * 2 * self.cell_size

                for k in range(0, self.model.size):
                    pos_z = (self.init_position + k) * 2 * self.cell_size

                    if not redraw:
                        cube = self.createCube(pos_x, pos_y, pos_z,
                                self.cell_size, self.grid_color, self.grid_thickness)
                        self.cube_node.attachNewNode(cube)
                        self.cubes += [ cube ]

                    current_mark = self.model.getMark(i, j, k)

                    if current_mark == GameModel.Marks.PLAYER_ONE:
                        mark = self.model_player_one.copyTo(self.marks_node)
                        mark.setColor(self.player_one_color) #TODO color model already
                    elif current_mark == GameModel.Marks.PLAYER_TWO:
                        mark = self.model_player_two.copyTo(self.marks_node)
                        mark.setColor(self.player_two_color)

                    else: # EMPTY cell
                        mark = self.model_empty.copyTo(self.marks_node)
                        mark.setColor(self.empty_color)

                    mark.setPos(pos_x, pos_y, pos_z)
                    self.marks += [ mark ]

    def show_pointer(self):

        self.pointer.hide()
        self.pointerCube_node.show()

    def hide_pointer(self):

        self.pointer.hide()
        self.pointerCube_node.hide()
        
    def refresh(self, task):
        '''Adds new marks.'''

        if self.model.refresh:
            self.drawPlayingField(True)
            self.model.refresh = False

        return Task.cont # Continuous task

      
    def move_pointer(self, task):
        '''Sets pointer.'''

        (ptr_x, ptr_y, ptr_z) = self.ca.getPointer()
        if (self.ca.isPointerValid()):
            #self.show_pointer()
            self.pointer_node.setPos(ptr_x, ptr_y, ptr_z)
        #else:
            #self.hide_pointer()

        return Task.cont # Continuous task

    def rotate(self, task):
        '''Rotates model.'''

        (rot_x, rot_y, rot_z) = self.ca.getRotation()

        self.root_x_node.setHpr(self.render.getHpr())
        self.aux_node.wrtReparentTo(self.root_x_node)
        self.root_x_node.setHpr(rot_x, rot_y, rot_z)
        self.ca.resetRotation()
        self.aux_node.wrtReparentTo(self.render)
        self.root_node.setHpr(self.aux_node.getHpr())
        
        # Get nearest integer position, place the PointerCube there:
        self.auxPtr_node.wrtReparentTo(self.root_node)
        pos = self.auxPtr_node.getPos()
        self.__ptrPos = [math.floor(pos.x/4)*4+2, math.floor(pos.y/4)*4+2, math.floor(pos.z/4)*4+2]
        self.pointerCube_node.setPos(math.floor(pos.x/4)*4+2, math.floor(pos.y/4)*4+2, math.floor(pos.z/4)*4+2)
        show = True
        for i in self.__ptrPos:
            if (i > 6 or i < -6):
                show = False
        if (show and self.ca.isPointerValid()):
            self.show_pointer()
        else:
            self.hide_pointer()
        self.auxPtr_node.wrtReparentTo(self.pointer_node)
        
        # Update text
        self.text.setText("Na tahu je " + self.model.getPlayer())
        
        return Task.cont # Continuous task

    def createCube(self, pos_x, pos_y, pos_z, size, color, thickness):
        '''Creates cube consisting only of edges. Is used for grid depiction.'''

        ls = LineSegs()

        ls.setColor(color)
        ls.setThickness(thickness)

        # front edges
        ls.moveTo(pos_x-size, pos_y-size, pos_z-size)
        ls.drawTo(pos_x+size, pos_y-size, pos_z-size)   
        ls.moveTo(pos_x+size, pos_y-size, pos_z-size)
        ls.drawTo(pos_x+size, pos_y-size, pos_z+size)   
        ls.moveTo(pos_x+size, pos_y-size, pos_z+size)
        ls.drawTo(pos_x-size, pos_y-size, pos_z+size)   
        ls.moveTo(pos_x-size, pos_y-size, pos_z+size)
        ls.drawTo(pos_x-size, pos_y-size, pos_z-size)   

        # side edges
        ls.moveTo(pos_x+size, pos_y-size, pos_z-size)
        ls.drawTo(pos_x+size, pos_y+size, pos_z-size)   
        ls.moveTo(pos_x+size, pos_y-size, pos_z+size)
        ls.drawTo(pos_x+size, pos_y+size, pos_z+size)   
        ls.moveTo(pos_x-size, pos_y-size, pos_z+size)
        ls.drawTo(pos_x-size, pos_y+size, pos_z+size)   
        ls.moveTo(pos_x-size, pos_y-size, pos_z-size)
        ls.drawTo(pos_x-size, pos_y+size, pos_z-size)   

        # back edges
        ls.moveTo(pos_x-size, pos_y+size, pos_z-size)
        ls.drawTo(pos_x+size, pos_y+size, pos_z-size)   
        ls.moveTo(pos_x+size, pos_y+size, pos_z-size)
        ls.drawTo(pos_x+size, pos_y+size, pos_z+size)   
        ls.moveTo(pos_x+size, pos_y+size, pos_z+size)
        ls.drawTo(pos_x-size, pos_y+size, pos_z+size)   
        ls.moveTo(pos_x-size, pos_y+size, pos_z+size)
        ls.drawTo(pos_x-size, pos_y+size, pos_z-size)   

        ls.moveTo(0.0, 0.0, 0.0)

        return ls.create()
    
    def getSelectedCoords(self):
        # +6 ) /3
        x = int((self.__ptrPos[0] + 6) / 3)
        y = int((self.__ptrPos[1] + 6) / 3)
        z = int((self.__ptrPos[2] + 6) / 3)
        if x == 4:
            x = 3
        if y == 4:
            y = 3
        if z == 4:
            z = 3
        return (x,y,z)
















