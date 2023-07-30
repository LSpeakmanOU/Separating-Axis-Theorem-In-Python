# The following is a port by Liam Speakman of the Separating Axis Theorem code from this article in python: https://dyn4j.org/2010/01/sat/
# This code does not implement curved collisions or containment
# vectors are represented by tuples and shapes are represented by lists of vertices as tuples
import math

def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]
def length(vec):
    return math.sqrt(dot(vec, vec))
def normalize(vec):
    l = length(vec)
    return (vec[0] / l, vec[1] / l)
def scale(vec, scalar):
    return (vec[0] * scalar, vec[1] * scalar)
def add(vec1, vec2):
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])
def sub(vec1, vec2):
    return (vec1[0] - vec2[0], vec1[1] - vec2[1])
def proj(a,b):
    s = dot(a,b) / dot(b,b)
    return scale(b, s)
def left_normal(vec):
    return (vec[1], -vec[0])
def right_normal(vec):
    return (-vec[1], vec[0])
def project_shape(shape, axis):
    axis_n = normalize(axis)
    min = dot(axis_n,shape[0])
    max = min
    for i in range(len(shape)):
        p = dot(axis_n, shape[i])
        if (p < min):
            min = p
        elif (p > max):
            max = p
    return (min, max)
def overlap(p1, p2):
    if p1[0] < p2[0] and p1[1] > p2[0]:
        return True
    if p2[0] < p1[0] and p2[1] > p1[0]:
        return True
    return False
def get_overlap(p1, p2): 
    if p1[0] < p2[0] and p1[1] > p2[0]:
        return p1[1] - p2[0]
    if p2[0] < p1[0] and p2[1] > p1[0]:
        return p2[1] - p1[0]
    return None

def get_axes(shape):
    axes = []
    shape_len = len(shape)
    for i in range(shape_len):
        p1 = shape[i]
        p2 = shape[(i + 1) % shape_len]

        edge = sub(p1,p2)
        normal = right_normal(edge)
        axes.append(normal)
    
    return axes
def sat(shape1, shape2):
    smallest_overlap = None
    smallest_axis = None
    smallest_direction = None
    axes = get_axes(shape1)
    
    for i in range(len(axes)):
        axis = axes[i]
        p1 = project_shape(shape1,axis)
        p2 = project_shape(shape2,axis)
        if not overlap(p1, p2):
            return False
        else:
            o = get_overlap(p1, p2)
            if (smallest_overlap == None or o < smallest_overlap):
                smallest_overlap = o
                smallest_axis = axis
                if p1[0] < p2[0]:
                    smallest_direction = -1
                else:
                    smallest_direction = 1
    axes = get_axes(shape2)
    
    for i in range(len(axes)):
        axis = axes[i]
        p1 = project_shape(shape1,axis)
        p2 = project_shape(shape2,axis)
        if not overlap(p1, p2):
            return False
        else:
            o = get_overlap(p1, p2)
            if (smallest_overlap == None or o < smallest_overlap):
                smallest_overlap = o
                smallest_axis = axis
                if p1[0] < p2[0]:
                    smallest_direction = -1
                else:
                    smallest_direction = 1

    return (smallest_overlap, smallest_axis, smallest_direction)