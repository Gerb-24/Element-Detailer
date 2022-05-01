from src.PyVMF import *
from classes import *
from main import *
from corners import cornersAndSidewalls
import os

def movePrototypeToSolid( solid: Solid, prototypeVMF: VMF, texture: str, method="side" ):

    prototypeDuplicate = createDuplicateVMF( prototypeVMF )

    if method == "side" or method == "bigside":
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

    prototypeVertexManipulationBoxes = PrototypeVertexManipulationBoxes( prototype=method )
    verticesToManipulate = prototypeVertexManipulationBoxes.createVerticesInBoxDict( prototypeDuplicate )
    verticesToManipulate.moveToZero()
    verticesToManipulate.moveToSolid( solid )
    return prototypeDuplicate

def detailElements( prototypeVMF: VMF, inputVMF: VMF, texture: str, method="side" ):
    detailedVMF = createDuplicateVMF( inputVMF )
    dummyVMF = new_vmf()
    if method == 'corner':
        return cornersAndSidewalls( prototypeVMF, inputVMF, texture )
    solids_to_remove = []
    for solid in detailedVMF.get_solids():
        if solid.has_texture( texture ):
            movedPrototypeVMF = movePrototypeToSolid( solid , prototypeVMF, texture, method=method )
            if movedPrototypeVMF is None:
                continue
            dummyVMF = addVMF( dummyVMF, movedPrototypeVMF )
            solids_to_remove.append( solid )
    detailedVMF = removeSolids( detailedVMF, solids_to_remove )
    detailedVMF = addVMF( detailedVMF, dummyVMF )
    return detailedVMF

def detailMultipleElements(fileName: str, preElementToDetailList: List):
    elementToDetailList = [ ElementToDetail(elem["prt"], elem["tex"], method=elem["mtd"] ) for elem in preElementToDetailList ]
    inputVMF = load_vmf(fileName)
    dummyVMF = createDuplicateVMF( inputVMF )
    for element in elementToDetailList:
        dummyVMF = detailElements(element.prototypeVMF, dummyVMF, element.texture, element.method)
    withoutExtension = os.path.splitext(fileName)[0]
    dummyVMF.export(f"{withoutExtension}_detailed.vmf")
