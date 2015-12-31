'''
Created on 2015年12月17日

@author: cdz
'''

from math import sin, cos, pi
import sys
try:
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
    from OpenGL.GL import *
except Exception as e:
    print(e)
    sys.exit()
    
def subdivide(r, latitude_num, longtitude_num): #latitude：纬度， longtitude：经度
    '''返回各个点相对于球心的位置向量'''
    '''由于纬度最高的两个点是极点，所以返回的数组为x[latitude_num + 1][longtitude_num][Δx, Δy, Δz]'''
    result = []
    result.append([[0, 0, r]] * longtitude_num)
    theta_list = [i * pi / latitude_num for i in range(1, latitude_num)]
    alpha_list = [(i << 1) * pi / longtitude_num for i in range(0, longtitude_num)]
    cos_theta_list = [cos(theta) for theta in theta_list]
    sin_theta_list = [sin(theta) for theta in theta_list]
    cos_alpha_list = [cos(alpha) for alpha in alpha_list]
    sin_alpha_list = [sin(alpha) for alpha in alpha_list]
    for i in range(0, latitude_num - 1):
        latitude_ring = []
        for j in range(0, longtitude_num):
            dz = r * cos_theta_list[i]
            lati_r = r * sin_theta_list[i]
            dx = lati_r * cos_alpha_list[j]
            dy = lati_r * sin_alpha_list[j]
            latitude_ring.append([dx, dy, dz])
        result.append(latitude_ring)
    result.append([[0, 0, -r]] * longtitude_num)
    return result
    
def draw_ball(center_x, center_y, center_z, offsets):
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for latitude_ring in offsets:
        for point in latitude_ring:
            x = center_x + point[0]
            y = center_y + point[1]
            z = center_z + point[2]
            glVertex3f(x, y, z)
    glEnd()
    
def texture_map():
    pass

if __name__ == '__main__':
    pass