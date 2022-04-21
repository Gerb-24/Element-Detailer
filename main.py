from src.PyVMF import *
import os
import numpy as np

class ElementToDetail:
    def __init__( self, prototypeVMF: str, texture: str, method="side" ):
        self.fileName = prototypeVMF
        self.prototypeName = os.path.basename(prototypeVMF)
        self.prototypeVMF = load_vmf(prototypeVMF)
        self.texture = texture
        self.method = method

    def serialize(self):
        return [ self.fileName ,self.texture, self.method ]

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

def removeSolids(vmf: VMF, solidsToRemove):
    solidsNotToRemove = []
    newVmf = new_vmf()
    entities = vmf.get_entities(include_solid_entities=True)
    for solid in vmf.get_solids():
        if solid not in solidsToRemove:
            solidsNotToRemove.append(solid)
    newVmf.add_solids(*solidsNotToRemove)
    newVmf.add_entities(*entities)
    return newVmf

def createDuplicateVMF(vmf: VMF):
    duplicateVMF = new_vmf()
    funcDetails = vmf.get_entities(include_solid_entities=True)
    copiedFuncDetails = [funcDetail.copy() for funcDetail in funcDetails]
    duplicateVMF.add_entities(*copiedFuncDetails)
    return duplicateVMF

def getDimensionsOfSolid( solid: Solid ):
    allVertices = solid.get_all_vertices()
    xMin = min([ vertex.x for vertex in allVertices ])
    yMin = min([ vertex.y for vertex in allVertices ])
    zMin = min([ vertex.z for vertex in allVertices ])
    xMax = max([ vertex.x for vertex in allVertices ])
    yMax = max([ vertex.y for vertex in allVertices ])
    zMax = max([ vertex.z for vertex in allVertices ])
    return xMin, xMax, yMin, yMax, zMin, zMax

def getOrientationOfSolid( solid: Solid, texture: str ):
    texturedSide = solid.get_texture_sides( texture )[0]
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
    else:
        return None

def checkIfTop( solid: Solid, texture: str ):
    texturedSide = solid.get_texture_sides( texture )[0]
    texturedSideVertices = texturedSide.get_vertices()
    _, _, _, _, _, zMax = getDimensionsOfSolid( solid )
    return all( vertex.z == zMax for vertex in texturedSideVertices )

def rotateSolidAroundZAxis(solid: Solid, deg: int):
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

def movePrototypeToSolid( solid: Solid, prototypeVMF: VMF, texture: str, method="side" ):

    prototypeDuplicate = createDuplicateVMF( prototypeVMF )

    if method == "side":
        orientationOfSolid = getOrientationOfSolid( solid, texture )
        if orientationOfSolid is None:
            return None

        orientationToRotationDict = {
            "-y": 0,
            "x": 90,
            "y": 180,
            "-x":270,
        }

        for solidToRotate in prototypeDuplicate.get_solids():
            rotateSolidAroundZAxis( solidToRotate, orientationToRotationDict[orientationOfSolid] )
    elif method == "top":
        if not checkIfTop( solid, texture ):
            return None

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

    # set to zero, note that the size of the prototype is 2*384^3
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
        vertex.move(0, 0, zMax)
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

def detailElements( prototypeVMF: VMF, toBeDetailedVMF: VMF, detailedVMF: VMF, texture: str, method="side" ):
    solids_to_remove = []
    for solid in toBeDetailedVMF.get_solids():
        if solid.has_texture( texture ):
            movedPrototypeVMF = movePrototypeToSolid( solid , prototypeVMF, texture, method=method )
            if movedPrototypeVMF is None:
                continue
            funcDetails = movedPrototypeVMF.get_entities(include_solid_entities=True)
            detailedVMF.add_entities(*funcDetails)
            solids_to_remove.append(solid)
    return solids_to_remove

def detailMultipleElements(fileName: str, elementToDetailList: List):
    solids_to_remove = []
    toBeDetailedVMF = load_vmf(fileName)
    detailedVMF = toBeDetailedVMF
    for element in elementToDetailList:
        solids_to_remove.extend( detailElements(element.prototypeVMF, toBeDetailedVMF, detailedVMF, element.texture, element.method) ) # This also does edit a lot of things
    detailedVMF = removeSolids(detailedVMF, solids_to_remove)
    withoutExtension = os.path.splitext(fileName)[0]
    detailedVMF.export(f"{withoutExtension}_detailed.vmf")
