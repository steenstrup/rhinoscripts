__author__ = 'Kasper H Steenstrup'

import rhinoscriptsyntax as rs
import Rhino.Geometry.Point3f as Point3f


def extend(s, mm_len):
    """
    Extend a ruled surface such that all the ruling are 400mm long
    :param s: A ruled surface
    :param mm_len: Desired Length of each ruling
    :return: Ruled surface with ruling length mm_len
    """

    u0, u1 = rs.SurfaceDomain(s, 0)
    v0, v1 = rs.SurfaceDomain(s, 1)

    deg_u, deg_v = rs.SurfaceDegree(s)

    no = 50
    d = (u1-u0)/float(no)
    if deg_u == 1:
        d = (v1-v0)/float(no)

    points0 = []
    points1 = []
    for t in range(0, no+1):
        if deg_u == 1:
            c = rs.ExtractIsoCurve(s, (u0, v0 + d*t), 0)
        else:
            c = rs.ExtractIsoCurve(s, (u0 + d*t, v0), 0)

        if c == []:
            continue

        L = (mm_len - rs.CurveLength(c))/2.0

        c0 = rs.ExtendCurveLength(c[0], 0, 0, L)
        if c0 is None:
            continue

        c1 = rs.ExtendCurveLength(c0, 0, 1, L)
        if c1 is None:
            continue

        points0.append(rs.CurveEndPoint(c1))
        points1.append(rs.CurveStartPoint(c1))
        rs.DeleteObject(c1)

    c0 = rs.AddCurve(points0)
    c1 = rs.AddCurve(points1)

    rs.AddLoftSrf([c0, c1], loft_type=2)
    rs.DeleteObject(c0)
    rs.DeleteObject(c1)

if __name__ == "__main__":
    surface = rs.GetObject("surface", filter=8)
    extend(surface, 400)