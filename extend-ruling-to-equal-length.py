"""
Extend a ruled surface shouch that all the ruling are 400mm long
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry.Point3f as Point3f

surface = rs.GetObject("surface",filter=8)

def extend(surface, mm_len):

    u0, u1 = rs.SurfaceDomain(surface, 0)
    v0, v1 = rs.SurfaceDomain(surface, 1)
    
    
    deg_u, deg_v = rs.SurfaceDegree(surface)
    
    if deg_u == 1:
        no = 50
        dv = (v1-v0)/float(no)
        
        points0 = []
        points1 = []
        for v in range(0, no+1):
            c = rs.ExtractIsoCurve(surface, (u0, v0 + dv*v), 0)
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
        
        rs.AddLoftSrf([c0,c1], loft_type=2)
        rs.DeleteObject(c0)
        rs.DeleteObject(c1)
    

extend(surface, 400)
