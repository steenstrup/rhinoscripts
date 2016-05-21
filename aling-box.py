__author__ = 'Kasper H Steenstrup'

import rhinoscriptsyntax as rs
import Rhino.Geometry.Vector3d as Vector3d
import math


def alingBlock(block_a, block_b, model_inside):
    """
    Scale box to the correct dimentions
    Align box a and what is inside to box b
    The dimention of the box is expected to be equal lenght
    :param block_a:
    :param block_b: block to align block_a to
    :param model_inside: models inside block_a
    """

    # Find center of box_a
    exp_a = rs.ExplodePolysurfaces(block_a)
    cen_a = Vector3d(0, 0, 0)
    for exp in exp_a:
        cen_a += rs.SurfaceAreaCentroid(exp)[0]
    cen_a /= 6.0

    # Find center of box_b
    exp_b = rs.ExplodePolysurfaces(block_b)
    cen_b = Vector3d(0, 0, 0)
    for exp in exp_b:
        cen_b += rs.SurfaceAreaCentroid(exp)[0]
    cen_b /= 6.0

    # Find side Lenght
    c = rs.DuplicateEdgeCurves(exp_a[0])
    L = float(rs.CurveLength(c[0]))

    def sqrt_length(a, b, c):
        return math.sqrt(a*a + b*b + c*c)

    def create_matrix(a, b, c, d):
        M = [[a[0], a[1], a[2], d[0]],
             [b[0], b[1], b[2], d[1]],
             [c[0], c[1], c[2], d[2]],
             [0, 0, 0, 1]]
        return M

    # find basic function of box_a
    basic_0 = cen_a - rs.SurfaceAreaCentroid(exp_a[0])[0]
    basic_0 /= sqrt_length(basic_0[0], basic_0[1], basic_0[2])

    basic_1 = rs.SurfaceAreaCentroid(exp_a[1])[0] - cen_a
    basic_1 /= sqrt_length(basic_1[0], basic_1[1], basic_1[2])

    basic_2 = cen_a - rs.SurfaceAreaCentroid(exp_a[4])[0]
    basic_2 /= sqrt_length(basic_2[0], basic_2[1], basic_2[2])

    # create tranformation matrix
    M = create_matrix(basic_0, basic_1, basic_2, [0,0,0])

    # scale
    rs.ScaleObjects([block_a] + model_inside, cen_a, [200/L,200/L,200/L])

    # move to [0,0,0]
    rs.MoveObjects([block_a] + model_inside, -cen_a)

    # rotate
    rs.TransformObjects([block_a] + model_inside, M)

    # move to object
    rs.MoveObjects([block_a] + model_inside, cen_b)

    rs.DeleteObjects(exp_a)
    rs.DeleteObjects(exp_b)

    rs.DeleteObjects(c)


if __name__ == "__main__":
    box_a = rs.GetObject("Pick box a")
    model_inside = rs.GetObjects("Align box a")
    box_b = rs.GetObject("Pick box to align to")
    alingBlock(box_a, box_b, model_inside)
