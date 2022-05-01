from src.PyVMF import *
import numpy as np
from classes import *
from main import *

class SideData:
    def __init__( self, side, solid ):
        self.solid = solid
        self.orientation = getOrientationOfSide( solid, side )
        self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax = getDimensionsOfSide( side )
        self.start, self.end = self.getStartEnd()
        self.heights = ( self.zMin, self.zMax )
        self.hasCommonEdge = {
            'start': False,
            'end': False,
        }

    def getStartEnd( self ):
        if  self.orientation == '-x':
            start = ( self.xMax, self.yMax )
            end = ( self.xMax, self.yMin )
        elif self.orientation == '-y':
            start = ( self.xMin, self.yMax )
            end = ( self.xMax, self.yMax )
            return ( start, end )
        elif self.orientation == 'x':
            start = ( self.xMax, self.yMin )
            end = ( self.xMax, self.yMax )
        elif self.orientation == 'y':
            start = ( self.xMax, self.yMax )
            end = ( self.xMin, self.yMax )
        return  ( start, end )

class CommonEdge:
    def __init__( self, sideList ):
        self.sideList = sideList
        self.orientationSet = { side.orientation for side in sideList }
        self.startSide = sideList[0]
        self.commonPoint = self.startSide.end
        self.checkPoint = self.startSide.start
        self.zMin, self.zMax = self.startSide.zMin, self.startSide.zMax

    def isOutside( self ):
        outsideCheckDict = {
                'x':    (self.checkPoint[0] < self.commonPoint[0]),
                'y':    (self.checkPoint[1] < self.commonPoint[1]),
                '-x':   (self.checkPoint[0] > self.commonPoint[0]),
                '-y':    (self.checkPoint[1] > self.commonPoint[1]),
        }

        return any([ outsideCheckDict[orientation] for orientation in self.orientationSet ])

    def getRotation( self ):
        orientationSet = self.orientationSet
        if orientationSet == {'-x', '-y'}:
            rotation = 0
        elif orientationSet == {'x', '-y'}:
            rotation = 90
        elif orientationSet == {'x', 'y'}:
            rotation = 180
        elif orientationSet == {'-x', 'y'}:
            rotation = 270

        return rotation

def createCommonEdgeList( sideDataList ):
    commonEdgeList = []
    checking_list = [ sideDataList[0] ]
    for index in range(1,len( sideDataList )):
        side1 = sideDataList[index]
        for side2 in checking_list:
            if  side1.end == side2.start and side1.heights == side2.heights:
                commonEdge = CommonEdge( [ side1, side2 ] )
                commonEdgeList.append( commonEdge )

                # update the sidedate information
                side1.hasCommonEdge['end'] = True
                side2.hasCommonEdge['start'] = True

            elif side1.start == side2.end and side1.heights == side2.heights:
                commonEdge = CommonEdge( [ side2, side1 ] )
                commonEdgeList.append( commonEdge )

                side1.hasCommonEdge['start'] = True
                side2.hasCommonEdge['end'] = True
        checking_list.append( side1 )
    return commonEdgeList

def addCorner( cornerVMF: VMF, commonEdge: CommonEdge, detailedVMF: VMF ):
    duplicateCornerVMF = createDuplicateVMF( cornerVMF )

    # Scale to 0

    TopVertexManipulationBox = VertexManipulationBox( -1024, 1024, -1024, 1024, 0, 2048 )
    BottomVertexManipulationBox = VertexManipulationBox( -1024, 1024, -1024, 1024, -2048, 0 )

    topVertices = TopVertexManipulationBox.getVerticesInBox( duplicateCornerVMF )
    bottomVertices = BottomVertexManipulationBox.getVerticesInBox( duplicateCornerVMF )

    for vertex in topVertices:
        vertex.move( 0, 0, -1024 )
    for vertex in bottomVertices:
        vertex.move( 0, 0, 1024 )

    for solidToRotate in duplicateCornerVMF.get_solids():
        rotateSolidAroundZAxis( solidToRotate, commonEdge.getRotation() )
    for solid in duplicateCornerVMF.get_solids():
        solid.move(*commonEdge.commonPoint, 0)

    for vertex in topVertices:
        vertex.move( 0, 0, commonEdge.zMax)
    for vertex in bottomVertices:
        vertex.move( 0, 0, commonEdge.zMin )

    funcDetails = duplicateCornerVMF.get_entities(include_solid_entities=True)
    detailedVMF.add_entities(*funcDetails)

def extractCorners( cornerVMF: VMF ):

    outsideSelectionBox = SelectionBox( -2048, 0, -2048, 0, -2048, 2048 )
    insideSelectionBox = SelectionBox( 0, 2048, 0, 2048, -2048, 2048 )

    outsideSelection = outsideSelectionBox.getSolidsInBox( cornerVMF )
    outsideCornerVMF = outsideSelection.createVMF()
    insideSelection = insideSelectionBox.getSolidsInBox( cornerVMF )
    insideCornerVMF = insideSelection.createVMF()

    outsideVertexManipulationBox = VertexManipulationBox( -2048, 0, -2048, 0, -2048, 2048 )
    insideVertexManipulationBox = VertexManipulationBox( 0, 2048, 0, 2048, -2048, 2048 )

    # center prototypes to 0
    outsideVertices = outsideVertexManipulationBox.getVerticesInBox( outsideCornerVMF )
    for vertex in outsideVertices:
        vertex.move( 1024, 1024, 0 )

    insideVertices = insideVertexManipulationBox.getVerticesInBox( insideCornerVMF )
    for vertex in insideVertices:
        vertex.move( -1024, -1024, 0 )

    return insideCornerVMF, outsideCornerVMF

def get_texture_solids( vmf: VMF, texture: str ):
    texture_solids = [ solid for solid in vmf.get_solids( include_solid_entities=False ) if solid.has_texture( texture ) ]
    return texture_solids

def cornersAndSidewalls( cornerVMF: VMF, inputVMF: VMF, wallTexture: str ):
    detailedVMF = createDuplicateVMF( inputVMF )
    dummyVMF = new_vmf()

    insideCornerVMF, outsideCornerVMF = extractCorners( cornerVMF )

    outsideSizeBrush = get_texture_solids( outsideCornerVMF, 'tools/toolsskip' )[0]
    _, outsideValue, _, _, _, _ = getDimensionsOfSolid( outsideSizeBrush )

    insideSizeBrush = get_texture_solids( insideCornerVMF, 'tools/toolsskip' )[0]
    insideValue, _, _, _, _, _ = getDimensionsOfSolid( insideSizeBrush )

    solids = detailedVMF.get_solids()
    sideDataList = []
    for solid in solids:
        if solid.has_texture(wallTexture):
            for side in solid.get_texture_sides( wallTexture ):
                sideDataList.append( SideData( side, solid ) )
    commonEdgeList = createCommonEdgeList( sideDataList )

    for commonEdge in commonEdgeList:
        if commonEdge.isOutside():
            addCorner( outsideCornerVMF, commonEdge, dummyVMF )
        else:
            addCorner( insideCornerVMF, commonEdge, dummyVMF )

    # Here we will add the new walls
    prototypeVMF = load_vmf('prototypes/bigside_prototype.vmf')
    prototypeSolid = prototypeVMF.get_solids()[0]
    wallFace = prototypeSolid.get_texture_sides( 'dev/reflectivity_10' )[0]
    wallFace.material = wallTexture.upper()

    sidewalls = []
    for sideData in sideDataList:
        prototypeDuplicate = createDuplicateVMF(prototypeVMF)
        # Rotate in the correct position
        orientationToRotationDict = {
            "-y": 0,
            "x": 90,
            "y": 180,
            "-x":270,
        }
        for solidToRotate in prototypeDuplicate.get_solids():
            rotateSolidAroundZAxis( solidToRotate, orientationToRotationDict[ sideData.orientation ] )


        prototypeVertexManipulationBoxes = PrototypeVertexManipulationBoxes( prototype='bigside' )
        verticesToManipulate = prototypeVertexManipulationBoxes.createVerticesInBoxDict( prototypeDuplicate )
        verticesToManipulate.moveToZero()
        verticesToManipulate.moveToSideData( sideData, outsideValue )

        sidewall = prototypeDuplicate.get_solids()[0]
        sidewalls.append( sidewall )

    dummyVMF.add_solids( *sidewalls )

    solidsToRemove = [ sideData.solid for sideData in sideDataList ]
    detailedVMF = removeSolids( detailedVMF, solidsToRemove )
    detailedVMF = addVMF( detailedVMF, dummyVMF )

    return detailedVMF

# cornerVMF = load_vmf('test_vmfs/umon_prototypes/umon_corner_prototype.vmf')
# wallTexture = 'dev/dev_blendmeasure2'
# inputVMF = load_vmf('test_vmfs/corners.vmf')
# detailedVMF = new_vmf()
#
# cornersAndSidewalls( cornerVMF, inputVMF, detailedVMF, wallTexture  )
