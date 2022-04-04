from src.PyVMF import *
prototypeVMF = load_vmf("umon_ws_prototype.vmf")
toBeDetailedVMF = load_vmf("umon_ws_test.vmf")
detailedVMF = new_vmf()
wallshotTexture = "CUSTOMDEV/DEV_MEASUREWALL01BLU"

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

def movePrototypeToSolid( solid, prototypeVMF ):
    topVertexManipulationBox = VertexManipulationBox( -512, 512, -512, 512, 0, 512)
    bottomVertexManipulationBox = VertexManipulationBox( -512, 512, -512, 512, -512, 0)
    backVertexManipulationBox = VertexManipulationBox( -512, 512, 0, 512, -512, 512)
    frontVertexManipulationBox = VertexManipulationBox( -512, 512, -512, 0, -512, 512 )
    startVertexManipulationBox = VertexManipulationBox( 0, 512, -512, 512, -512, 512)
    endVertexManipulationBox = VertexManipulationBox( -512, 0, -512, 512, -512, 512)

    prototypeDuplicate = createDuplicateVMF(prototypeVMF)
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
