from src.PyVMF import *
import numpy as np
from classes import *
from main import *

ramp_vmf = load_vmf('test_vmfs/ramp_test.vmf')
texture = 'orange_dev/dev_measurewall_green03'
dummyVMF = new_vmf()
for solid in ramp_vmf.get_solids():
    if not solid.has_texture(texture):
        continue
    texturedSide = solid.get_texture_sides( texture )[0]
    xMin, xMax, yMin, yMax, zMin, zMax = getDimensionsOfSide( texturedSide )
    _, _, _, _, zMins, _ = getDimensionsOfSolid( solid )

    def getRampDirection( side, zMin, Zmax ):
        sideVertices = texturedSide.get_vertices()
        # we have either two zMax vertices or two zMin vertices in sideVertices
        maxVerts = [vertex for vertex in sideVertices if vertex.z == zMax]
        if len(maxVerts) == 2:
            if maxVerts[0].x == maxVerts[1].x:
                if maxVerts[0].x == xMax:
                    direction = 'x'
                else:
                    direction = '-x'
            else:
                if maxverts[0].y == yMax:
                    direction = 'y'
                else:
                    direction = '-y'
        else:
            minVerts = [vertex for vertex in sideVertices if vertex.z == zMin]
            if minVerts[0].x == minVerts[1].x:
                if minVerts[0].x == xMax:
                    direction = '-x'
                else:
                    direction = 'x'
            else:
                if minVerts[0].y == yMax:
                    direction = '-y'
                else:
                    direction = 'y'
        return direction



    proto_vmf = load_vmf('prototypes/umon/umon_ss_prototype.vmf')
    pmvb = PrototypeVertexManipulationBoxes(prototype='top')
    vtm = pmvb.createVerticesInBoxDict(proto_vmf)
    vtm.moveToZero()

    vd = vtm.verticesDict

    for vertex in vd['y']:
        vertex.move( 0, yMax, 0 )
    for vertex in vd['-y']:
        vertex.move( 0, yMin, 0 )

    for vertex in vd['x']:
        vertex.move( xMax, 0, 0 )
    for vertex in vd['-x']:
        vertex.move( xMin, 0, 0 )

    direction = getRampDirection( texturedSide, zMin, zMax )

    for vertex in vd['z']:
        if direction == 'x':
            vertex.move( 0, 0, (zMax-zMin)/(xMax-xMin)*(vertex.x - xMin)+zMin )
        elif direction == 'y':
            vertex.move( 0, 0, (zMax-zMin)/(yMax-yMin)*(vertex.y - yMin)+zMin )
        elif direction == '-x':
            vertex.move( 0, 0, (zMin-zMax)/(xMax-xMin)*(vertex.x - xMin)+zMax )
        elif direction == '-y':
            vertex.move( 0, 0, (zMin-zMax)/(yMax-yMin)*(vertex.y - yMin)+zMax )

    for vertex in vd['-z']:
        vertex.move( 0, 0, zMins )

    dummyVMF = addVMF( dummyVMF, proto_vmf )

dummyVMF.export('test_vmfs/ramp_test_detailed.vmf')
