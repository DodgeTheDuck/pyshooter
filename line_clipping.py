from vector import Vector

# check if line segment intersects triangle using Cyrus Beck algorithm
# I converted this in a fairly brain dead way from C++ found here...
# https://www.geeksforgeeks.org/line-clipping-set-2-cyrus-beck-algorithm/
# TODO: work out how it works and hopefully optimise it better for Python
# BUG: 
#       it appears to not be 100% accurate, but it is close. 
#       I have a feeling there's some int/float shenanigans going on.
#       Or I miss-typed something when converting from C++...
def cyrus_beck_clip(vertices: list[Vector], line_from: Vector, line_to: Vector) -> bool:
  
    n = len(vertices)
    # normals initialized dynamically(can do it statically also, doesn't matter)
    normals: list[Vector] = [Vector(0, 0) for i in range(n)]
    numerator: list[float] = [0 for i in range(n)]
    denominator: list[float] = [0 for i in range(n)]
    tE: list[float] = [] 
    tL: list[float] = []
    t: list[float] = [0.0 for i in range(n)]

    # calculating P1 - P0
    P1_P0: Vector = Vector(line_to.x - line_from.x, line_to.y - line_from.y)
  
    # initializing all values of P0 - PEi
    P0_PEi: list[Vector] = [Vector(0, 0) for i in range(n)]
  
    # calculating the values of P0 - PEi for all edges
    for i in range(n):
        normals[i].y = vertices[(i + 1) % n].x - vertices[i].x
        normals[i].x = vertices[i].y - vertices[(i + 1) % n].y
        #normals[i] = Vector.Normalise(normals[i])
        # calculating PEi - P0, so that the
        # denominator won't have to multiply by -1
        P0_PEi[i].x = vertices[i].x - line_from.x  
        # while calculating 't'
        P0_PEi[i].y = vertices[i].y - line_from.y

        numerator[i] = Vector.Dot(normals[i], P0_PEi[i])
        denominator[i] = Vector.Dot(normals[i], P1_P0)
  
        if(denominator[i] == 0): 
            tL.append(t[i])
            continue

        t[i] = float(numerator[i]) / float(denominator[i])
  
        if (denominator[i] > 0):
            tE.append(t[i])
        else:
            tL.append(t[i])
    
    tE.append(0.0)
    tL.append(1.0)

    temp = (max(tE), min(tL))      
  
    # entering 't' value cannot be
    # greater than exiting 't' value,
    # hence, this is the case when the line
    # is completely outside
    return temp[0] <= temp[1]
          
    # Calculating the coordinates in terms of x and y
    # newPair[0].first
    #     t
    #     = (float)line[0].first
    #       + (float)P1_P0.first * (float)temp[0];
    # newPair[0].second
    #     = (float)line[0].second
    #       + (float)P1_P0.second * (float)temp[0];
    # newPair[1].first
    #     = (float)line[0].first
    #       + (float)P1_P0.first * (float)temp[1];
    # newPair[1].second
    #     = (float)line[0].second
    #       + (float)P1_P0.second * (float)temp[1];
    # cout << '(' << newPair[0].first << ", "
    #      << newPair[0].second << ") ("
    #      << newPair[1].first << ", "
    #      << newPair[1].second << ")";
  
    #return newPair;