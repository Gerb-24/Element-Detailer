from src.PyVMF import *
import numpy as np

def removeSolids(vmf: VMF, solidsToRemove):
    vmf.world.solids = [ solid for solid in vmf.world.solids if solid not in solidsToRemove ]
    return vmf

def addVMF( vmf: VMF, vmf_to_add: VMF ):
    total_vmf = createDuplicateVMF( vmf )

    #add solids
    solids = vmf_to_add.get_solids( include_solid_entities=False )
    copiedSolids = [ solid.copy() for solid in solids ]
    total_vmf.add_solids(*copiedSolids)

    # add entities
    entities = vmf_to_add.get_entities( include_solid_entities=True )
    copiedEntities = [ entity.copy() for entity in entities ]
    total_vmf.add_entities(*copiedEntities)

    return total_vmf

def createDuplicateVMF(vmf: VMF):
    duplicateVMF = new_vmf()

    # add solids
    solids = vmf.get_solids( include_solid_entities=False )
    copiedSolids = [ solid.copy() for solid in solids ]
    duplicateVMF.add_solids(*copiedSolids)

    # add entities
    entities = vmf.get_entities( include_solid_entities=True )
    copiedEntities = [ entity.copy() for entity in entities ]
    duplicateVMF.add_entities(*copiedEntities)
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

def getOrientationOfSide( solid: Solid, side: Side ):
    sideVertices = side.get_vertices()
    xMin, xMax, yMin, yMax, _, _ = getDimensionsOfSolid( solid )
    if all( vertex.y == yMin for vertex in sideVertices ):
        return "-y"
    if all( vertex.x == xMax for vertex in sideVertices ):
        return "x"
    if all( vertex.y == yMax for vertex in sideVertices ):
        return "y"
    if all( vertex.x == xMin for vertex in sideVertices ):
        return "-x"
    else:
        return None

def getDimensionsOfSide( side: Side ):
    allVertices = side.get_vertices()
    xMin = min([ vertex.x for vertex in allVertices ])
    yMin = min([ vertex.y for vertex in allVertices ])
    zMin = min([ vertex.z for vertex in allVertices ])
    xMax = max([ vertex.x for vertex in allVertices ])
    yMax = max([ vertex.y for vertex in allVertices ])
    zMax = max([ vertex.z for vertex in allVertices ])
    return xMin, xMax, yMin, yMax, zMin, zMax
