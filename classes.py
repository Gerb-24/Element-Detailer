from src.PyVMF import *
from main import *
import numpy as np
import os

class PrototypeVertexManipulationBoxes:
    '''instantiates VMBs for all directions, depending on the prototype'''
    def __init__( self, prototype='side' ):
        self.prototype = prototype
        self.boxes = self.createBoxesDict()

    def createBoxesDict( self ):
        if self.prototype == 'side' or self.prototype == 'top':
            prototypeDict = {
                'x':   VertexManipulationBox( 0, 512, -512, 512, -512, 512 ),
                'y':    VertexManipulationBox( -512, 512, 0, 512, -512, 512 ),
                'z':    VertexManipulationBox( -512, 512, -512, 512, 0, 512 ),
                '-x':   VertexManipulationBox( -512, 0, -512, 512, -512, 512 ),
                '-y':   VertexManipulationBox( -512, 512, -512, 0, -512, 512 ),
                '-z':   VertexManipulationBox( -512, 512, -512, 512, -512, 0 ),
            }
            return prototypeDict
        elif self.prototype == 'bigside':
            prototypeDict = {
                'x':   VertexManipulationBox( 0, 1024, -1024, 1024, -1024, 1024 ),
                'y':    VertexManipulationBox( -1024, 1024, 0, 1024, -1024, 1024 ),
                'z':    VertexManipulationBox( -1024, 1024, -1024, 1024, 0, 1024 ),
                '-x':   VertexManipulationBox( -1024, 0, -1024, 1024, -1024, 1024 ),
                '-y':   VertexManipulationBox( -1024, 1024, -1024, 0, -1024, 1024 ),
                '-z':   VertexManipulationBox( -1024, 1024, -1024, 1024, -1024, 0 ),
            }
            return prototypeDict

    def createVerticesInBoxDict( self, vmf: VMF ):
        '''Creates a dictionary of lists of vertices that are contained in the given VMB'''
        verticesDict = { key: self.boxes[key].getVerticesInBox( vmf ) for key in self.boxes }
        return VerticesToManipulate( verticesDict, prototype=self.prototype )

class VertexManipulationBox:
    ''' a box that lets us manipulate the vertices in it'''
    def __init__( self, xMin, xMax, yMin, yMax, zMin, zMax ):
        self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax = xMin, xMax, yMin, yMax, zMin, zMax

    def getVerticesInBox( self, vmf: VMF ):
        allVertices = []
        for solid in vmf.get_solids():
            allVertices.extend( solid.get_all_vertices() )
        verticesInBox = []
        for vertex in allVertices:
            if self.xMin < vertex.x < self.xMax and self.yMin < vertex.y < self.yMax and self.zMin < vertex.z < self.zMax:
                verticesInBox.append( vertex )
        return verticesInBox

class VerticesToManipulate:
    def __init__( self, verticesDict, prototype='side' ):
        self.prototype = prototype
        self.verticesDict = verticesDict

    def moveToZero( self ):
        def getMove( direction, value ):
            moveDict = {
            'x': (value, 0, 0),
            'y': (0, value, 0),
            'z': (0, 0, value),
            '-x': (-value, 0, 0),
            '-y': (0, -value, 0),
            '-z': (0, 0, -value),
            }
            return moveDict[ direction ]
        if self.prototype == 'side' or self.prototype == 'top':
            # set to zero, note that the size of the prototype is 2*384^3
            for direction in self.verticesDict:
                for vertex in self.verticesDict[ direction ]:
                    vertex.move( *getMove( direction, -384 ) )
        if self.prototype == 'bigside':
            # set to zero, note that the size of the prototype is 2*768^3
            for direction in self.verticesDict:
                for vertex in self.verticesDict[ direction ]:
                    vertex.move( *getMove( direction, -768 ) )

    def moveToSideData( self, sideData, sizeValue ):
        for vertex in self.verticesDict['z']:
            vertex.move(0, 0, sideData.zMax)
        for vertex in self.verticesDict['-z']:
            vertex.move(0, 0, sideData.zMin)

        moveDict = {
            'x': 0,
            'y': 0,
            '-x': 0,
            '-y':0,
        }

        isPositiveDict = {
            'x': True,
            'y': True,
            '-x': False,
            '-y': False,
        }
        directionDict = {
            'x':    {
                'start': '-y',
                'end': 'y',
                'opposite': '-x'
                },
            'y':    {
                'start': 'x',
                'end': '-x',
                'opposite': '-y'
                },
            '-x':   {
                'start': 'y',
                'end': '-y',
                'opposite': 'x'
                },
            '-y':   {
                'start': '-x',
                'end': 'x',
                'opposite': 'y'
                 },
            }
        if sideData.hasCommonEdge['start']:
            moveDict[directionDict[sideData.orientation]['start']] = -sizeValue if isPositiveDict[ directionDict[sideData.orientation]['start'] ] else sizeValue
        if sideData.hasCommonEdge['end']:
            moveDict[directionDict[sideData.orientation]['end']] = -sizeValue if isPositiveDict[ directionDict[sideData.orientation]['end'] ] else sizeValue
        moveDict[directionDict[sideData.orientation]['opposite']] = -256 if isPositiveDict[ sideData.orientation ] else 256

        totalMoveDict = {
            'x':    ( sideData.xMax + moveDict['x'], 0, 0 ),
            'y':    ( 0, sideData.yMax + moveDict['y'], 0 ),
            '-x':   ( sideData.xMin + moveDict['-x'], 0, 0 ),
            '-y':   ( 0, sideData.yMin + moveDict['-y'], 0 ),
            }

        orientationList = [ 'x', 'y', '-x', '-y' ]
        for orientation in orientationList:
            for vertex in self.verticesDict[ orientation ]:
                vertex.move(*totalMoveDict[ orientation ])

    def moveToSolid( self, solid: Solid ):
        xMin, xMax, yMin, yMax, zMin, zMax = getDimensionsOfSolid( solid )
        for vertex in self.verticesDict['z']:
            vertex.move( 0, 0, zMax )
        for vertex in self.verticesDict['-z']:
            vertex.move( 0, 0, zMin )

        for vertex in self.verticesDict['y']:
            vertex.move( 0, yMax, 0 )
        for vertex in self.verticesDict['-y']:
            vertex.move( 0, yMin, 0 )

        for vertex in self.verticesDict['x']:
            vertex.move( xMax, 0, 0 )
        for vertex in self.verticesDict['-x']:
            vertex.move( xMin, 0, 0 )

class ElementToDetail:
    def __init__( self, prototypeVMF: str, texture: str, method="side" ):
        self.fileName = prototypeVMF
        self.prototypeName = os.path.basename(prototypeVMF)
        self.prototypeVMF = load_vmf(prototypeVMF)
        self.texture = texture
        self.method = method

    def serialize(self):
        return { "prt": self.fileName, "tex": self.texture, "mtd": self.method }

class SelectionBox:
    def __init__( self, xMin, xMax, yMin, yMax, zMin, zMax ):
        self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax = xMin, xMax, yMin, yMax, zMin, zMax

    def getSolidsInBox( self, vmf: VMF ):

        def checkVerticesInBox( vertices ):
            return any([ (self.xMin < vertex.x < self.xMax and self.yMin < vertex.y < self.yMax and self.zMin < vertex.z < self.zMax) for vertex in vertices])
        # Get the solids in the box
        solidsInBox = []
        solids = vmf.get_solids( include_solid_entities=False )
        for solid in solids:
            vertices = solid.get_only_unique_vertices()
            if checkVerticesInBox( vertices ):
                solidsInBox.append( solid )

        # Get the solid entities in the box
        entitiesInBox = []
        entities = vmf.get_entities( include_solid_entities=True )
        for entity in entities:
            for solid in entity.solids:
                vertices = solid.get_only_unique_vertices()
                if checkVerticesInBox( vertices ):
                    entitiesInBox.append( entity )
                    break
        return Selection( solidsInBox, entitiesInBox )

class Selection:
    def __init__( self, solids, entities ):
        self.solids = solids
        self.entities = entities

    def createVMF( self ):
        selectionVMF = new_vmf()

        # solids
        copiedSolids = [ solid.copy() for solid in self.solids ]
        selectionVMF.add_solids( *copiedSolids )

        # entities
        copiedEntities = [ entity.copy() for entity in self.entities ]
        selectionVMF.add_entities(*copiedEntities)

        return  selectionVMF
