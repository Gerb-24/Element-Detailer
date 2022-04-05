from src.PyVMF import *
import numpy as np

prototypeVMF = load_vmf("umon_ws_prototype.vmf")
toBeDetailedVMF = load_vmf("umon_ws_test.vmf")
detailedVMF = new_vmf()
texture = "CUSTOMDEV/DEV_MEASUREWALL01BLU"

def createDuplicateVMF(vmf):
    duplicateVMF = new_vmf()
    funcDetails = vmf.get_entities(include_solid_entities=True)
    copiedFuncDetails = [funcDetail.copy() for funcDetail in funcDetails]
    duplicateVMF.add_entities(*copiedFuncDetails)
    return duplicateVMF

class VertexManipulationBox:
    def __init__( self, xMin, xMax, yMin, yMax, zMin, zMax ):
        self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax = xMin, xMax, yMin, yMax, zMin, zMax

    def getVerticesInBox( self, vmf ):
        allVertices = []
        for solid in vmf.get_solids():
            allVertices.extend(solid.get_all_vertices())
        verticesInBox = []
        for vertex in allVertices:
            if self.xMin < vertex.x < self.xMax and self.yMin < vertex.y < self.yMax and self.zMin < vertex.z < self.zMax:
                verticesInBox.append( vertex )
        return verticesInBox

def getDimensionsOfSolid( solid ):
    allVertices = solid.get_all_vertices()
    xMin = min([ vertex.x for vertex in allVertices ])
    yMin = min([ vertex.y for vertex in allVertices ])
    zMin = min([ vertex.z for vertex in allVertices ])
    xMax = max([ vertex.x for vertex in allVertices ])
    yMax = max([ vertex.y for vertex in allVertices ])
    zMax = max([ vertex.z for vertex in allVertices ])
    return xMin, xMax, yMin, yMax, zMin, zMax

def getOrientationOfSolid( solid ):
    texturedSide = solid.get_texture_sides(texture)[0]
    texturedSideVertices = texturedSide.get_vertices()
    xMin, xMax, yMin, yMax, _, _ = getDimensionsOfSolid( solid )
    if all( vertex.y == yMin for vertex in texturedSideVertices ):
        return "-y"
    if all( vertex.x == xMax for vertex in texturedSideVertices ):
        return "x"
    if all( vertex.y == yMax for vertex in texturedSideVertices ):
        return "y"
    if all( vertex.x == xMin for vertex in texturedSideVertices ):
        return "-x"

def rotateSolidAroundZAxis(solid: Solid, deg):
    solid.rotate_z(Vertex( 0, 0, 0), deg )
    rad = deg/360*2*np.pi
    rotMat = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])
    for side in solid.get_sides():
        uaxisArray = np.array([float(side.uaxis.x), float(side.uaxis.y), float(side.uaxis.z)])
        uaxisArray = rotMat.dot(uaxisArray)
        side.uaxis.x, side.uaxis.y, side.uaxis.z = str(uaxisArray[0]), str(uaxisArray[1]), str(uaxisArray[2])

        vaxisArray = np.array([float(side.vaxis.x), float(side.vaxis.y), float(side.vaxis.z)])
        vaxisArray = rotMat.dot(vaxisArray)
        side.vaxis.x, side.vaxis.y, side.vaxis.z = str(vaxisArray[0]), str(vaxisArray[1]), str(vaxisArray[2])


def movePrototypeToSolid( solid, prototypeVMF ):

    prototypeDuplicate = createDuplicateVMF(prototypeVMF)
    orientationOfSolid = getOrientationOfSolid( solid )

    orientationToRotationDict = {
        "-y": 0,
        "x": 90,
        "y": 180,
        "-x":270,
    }

    for solidToRotate in prototypeDuplicate.get_solids():
        rotateSolidAroundZAxis( solidToRotate, orientationToRotationDict[orientationOfSolid] )

    topVertexManipulationBox = VertexManipulationBox( -512, 512, -512, 512, 0, 512)
    bottomVertexManipulationBox = VertexManipulationBox( -512, 512, -512, 512, -512, 0)
    backVertexManipulationBox = VertexManipulationBox( -512, 512, 0, 512, -512, 512)
    frontVertexManipulationBox = VertexManipulationBox( -512, 512, -512, 0, -512, 512 )
    startVertexManipulationBox = VertexManipulationBox( 0, 512, -512, 512, -512, 512)
    endVertexManipulationBox = VertexManipulationBox( -512, 0, -512, 512, -512, 512)

    topVertices = topVertexManipulationBox.getVerticesInBox(prototypeDuplicate)
    bottomVertices = bottomVertexManipulationBox.getVerticesInBox(prototypeDuplicate)
    backVertices = backVertexManipulationBox.getVerticesInBox(prototypeDuplicate)
    frontVertices = frontVertexManipulationBox.getVerticesInBox(prototypeDuplicate)
    startVertices = startVertexManipulationBox.getVerticesInBox(prototypeDuplicate)
    endVertices = endVertexManipulationBox.getVerticesInBox(prototypeDuplicate)


    # note that the size of the prototype is 2*384^3

    # set to zero
    for vertex in topVertices:
        vertex.move(0, 0, -384)
    for vertex in backVertices:
        vertex.move(0, -384, 0)
    for vertex in startVertices:
        vertex.move(-384, 0, 0)
    for vertex in bottomVertices:
        vertex.move(0, 0, 384)
    for vertex in frontVertices:
        vertex.move(0, 384, 0)
    for vertex in endVertices:
        vertex.move(384, 0, 0)

    xMin, xMax, yMin, yMax, zMin, zMax = getDimensionsOfSolid( solid )

    for vertex in topVertices:
        vertex.move(0, 0, 1024)
    for vertex in backVertices:
        vertex.move(0, yMax, 0)
    for vertex in startVertices:
        vertex.move(xMax, 0, 0)
    for vertex in bottomVertices:
        vertex.move(0, 0, zMin)
    for vertex in frontVertices:
        vertex.move(0, yMin, 0)
    for vertex in endVertices:
        vertex.move(xMin, 0, 0)

    return prototypeDuplicate

for solid in toBeDetailedVMF.get_solids():
    movedPrototypeVMF = movePrototypeToSolid( solid , prototypeVMF )
    funcDetails = movedPrototypeVMF.get_entities(include_solid_entities=True)
    detailedVMF.add_entities(*funcDetails)
detailedVMF.export("umon_ws_prototype_duplicate.vmf")
